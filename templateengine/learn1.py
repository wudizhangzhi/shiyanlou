#coding=utf8

'''
<p>Welcome, Charlie!</p>
<p>Products:</p>
<ul>
    <li>Apple: $1.00</li>
    <li>Fig: $1.50</li>
    <li>Pomegranate: $3.25</li>
</ul>
'''
# The main HTML for the whole page.
PAGE_HTML = """
<p>Welcome, {name}!</p>
<p>Products:</p>
<ul>
{products}
</ul>
"""

PRODUCT_HTML = "<li>{prodname}: {price}</li>"

def make_page(username, products):
    product_html = ''
    for prodname, price in products:
        product_html += PRODUCT_HTML.format(prodname=prodname, price=price)
    html = PAGE_HTML.format(name=username, products=product_html)
    return html

if __name__ == '__main__':
    html = make_page('tom', [('prod1','100'),('prod2','333')])
    print html
    