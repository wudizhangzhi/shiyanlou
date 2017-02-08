#coding=utf8
import re
import requests


class CodeBuilder(object):
    """
    编译模板代码
    """
    INDENT_STEP = 4 #PEP8 
    def __init__(self, indent=0):
        self.indent_level = indent
        self.code = []

    def add_line(self, line):
        self.code.extend([' '*self.indent_level + line + '\n'])

    def indent(self): #增加缩进
        self.indent_level += self.INDENT_STEP

    def dedent(self): #减少缩进
        self.indent_level -= self.INDENT_STEP

    def add_section(self): #增加代码块
        section = CodeBuilder(indent=self.indent_level)
        self.code.append(section)
        return section

    def __str__(self):
        # self.code将会存在CodeBuild对象，会迭代
        return ''.join([str(c) for c in self.code])

    def get_globals(self):
        assert self.indent_level == 0
        python_source = str(self) #代码字符串
        global_namespace = {} 
        #TODO 
        print python_source
        print '--------------------------------------'
        exec(python_source, global_namespace) #执行代码，收集字符串代码中定义的全局变量
        return global_namespace


class TempliteSyntaxError(Exception):
    """模板语法错误"""
    pass

class Templite(object):
    """
    模板
    """
    def __init__(self, template_text, *contexts):
        self.context = {}
        for context in contexts:
            self.context.update(context)
        code = CodeBuilder()
        code.add_line('def render_function(context,do_dots):')
        code.indent()
        vars_code = code.add_section()
        code.add_line('result = []')
        code.add_line('append_result = result.append')
        code.add_line('extend_result = result.extend')
        code.add_line('to_str = str')

        self.all_vars = set() # 所有变量
        self.loop_vars = set() # 循环变量


        # 缓存
        buffered = []
        def flush_out():
            """将缓存的字符串写入CodeBuilder"""
            if len(buffered) == 1:
                code.add_line('append_result(%s)' % buffered[0])
            elif len(buffered) > 1:
                code.add_line('extend_result([%s])' % ','.join(buffered))
            del buffered[:]

        ops_stack = []
        # (?s) 单行模式 (?m)多行模式, 即.匹配所有字符，包括\n
        tokens = re.split(r'(?s)({%.*?%}|{{.*?}}|{#.*?#})', template_text)
        for token in tokens:
            if token.startswith('{#'):
                # ingore
                continue
            elif token.startswith('{{'):
                expr = self._expr_code(token[2:-2].strip())
                buffered.append('to_str(%s)' % expr)
            
            elif token.startswith('{%'):
                flush_out()
                words = token[2:-2].split()
                if words[0] == 'if':
                    if len(words) !=2:
                        self._syntax_error("Don't understand if", token)
                    ops_stack.append('if')
                    code.add_line('if %s:' % self._expr_code(words[1]))
                    code.indent()

                    
                elif words[0] == 'for':
                    if len(words) != 4 and words[2] != 'in':
                        self._syntax_error("Don't understand for", token)
                    self._variable(words[1], self.loop_vars)
                    code.add_line('for c_%s in %s:' % (words[1], self._expr_code(words[3])))
                    code.indent()
                    ops_stack.append('for')
                    
                elif words[0] == 'end':
                    ops_stack.pop()
                    code.dedent()
                    
                else:
                    self._syntax_error("Don't understand tag", words[0])

            else:#页面正常html
                if token:
                    buffered.append(repr(token))
        if ops_stack:
            self._syntax_error('多余的tag', ops_stack[-1])

        flush_out()
        for var_name in self.all_vars - self.loop_vars:
            vars_code.add_line("c_%s = context['%s']" % (var_name, var_name))
        code.add_line("return ''.join(result)")
        code.dedent()
        self._render_function = code.get_globals()['render_function']


    def _expr_code(self, expr):
        """TODO 解释语法代码"""
        if '|' in expr:# a|b|c
            pipes = expr.split('|')
            code = self._expr_code(pipes[0])
            for func in pipes[1:]:
                self._variable(func, self.all_vars)
                code = 'c_%s(%s)' % (func, code)

        elif '.' in expr:# a.b.c
            dots = expr.split('.')
            code = self._expr_code(dots[0])
            args = ','.join(repr(i) for i in dots[1:])
            code = 'do_dots(%s, %s)' % (code, args)

        else:# a
            self._variable(expr, self.all_vars)
            code = 'c_%s' % expr
        return code

    def _syntax_error(self, msg, thing):
        """%r = repr, %s = str"""
        raise TempliteSyntaxError('%s:%r' % (msg, thing))

    def _variable(self, name, vars_set):
        """判断变量名是否可用，并保存到传入的var_set"""
        if not re.findall(r'[_a-zA-Z][_0-9a-zA-Z]*$', name):
            self._syntax_error('Not a valid name', name)
        vars_set.add(name)

    def render(self, context=None):
        """返回处理后的html"""
        render_context = dict(self.context)
        if context:
            render_context.update(context)
        return self._render_function(render_context, self._do_dots)

    def _do_dots(self, value, *dots):
        """CodeBuilder处理类似data.column.row.name的语法"""
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value[dot]
            if callable(value):
                value = value()
        return value






TEMPLATE = """
    <p>Welcome, {{user_name}}!</p>
    <p>Products:</p>
    <ul>
    {% for product in product_list %}
        <li>{{ product.name }}:
            {{ product.price|format_price }}</li>
    {% endfor %}
    </ul>
"""

def test():
    template = '''
        <p>Welcome, {{user_name}}!</p>
        <p>wow!{{test.age}}!</p>
        <p>wow!{{test.name|upper}}!</p>
        {% if test.age %}
        <h1>you are {{test.age}}</h1>
        {% end %}

        {% for product in product_list %}
        <li>{{product.name}}</li>
        {% end %}
    '''
    t = Templite(template,{'upper':str.upper})
    html = t.render({'user_name':'Tom',
        'test':{'age':20,'name':'jack'},
        'product_list':[{'name':'first'}]})
    print html

if __name__ == '__main__':
    test()