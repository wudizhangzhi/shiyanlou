

#!/bin/bash 
#export DYLD_FALLBACK_LIBRARY_PATH="${HOME}/wine/wine-1.2/lib:/usr/X11/lib:/usr/ lib" 
export TERM=xterm-color 
export CLICOLOR=1 
export LSCOLORS=ExFxCxDxBxegedabagacad 
export EDITOR=vi 
#export CDPATH=$CDPATH:/Users/auxten/Documents/Codes/ 
use_color=false 
# Set colorful PS1 only on colorful terminals. 
# dircolors --print-database uses its own built-in database 
# instead of using /etc/DIR_COLORS.  Try to use the external file 
# first to take advantage of user additions.  Use internal bash 
# globbing instead of external grep binary. 
safe_term=${TERM//[^[:alnum:]]/?}   # sanitize TERM 
match_lhs="" 
[[ -f ~/.dir_colors   ]] && match_lhs="${match_lhs}$(<~/.dir_colors)" 
[[ -f /etc/DIR_COLORS ]] && match_lhs="${match_lhs}$(</etc/DIR_COLORS)" 
[[ -z ${match_lhs}    ]] \
    && type -P dircolors >/dev/null \
    && match_lhs=$(dircolors --print-database) 
[[ $'\n'${match_lhs} == *$'\n'"TERM "${safe_term}* ]] && use_color=true 
if ${use_color} ; then     
# Enable colors for ls, etc.  Prefer ~/.dir_colors #64489     
    if type -P dircolors >/dev/null ; then         
        if [[ -f ~/.dir_colors ]] ; then             
            eval $(dircolors -b ~/.dir_colors)         
        elif [[ -f /etc/DIR_COLORS ]] ; then             
            eval $(dircolors -b /etc/DIR_COLORS)         
        fi     
    fi     
if [[ ${EUID} == 0 ]] ; then
    PS1='\[\033[01;31m\]\h\[\033[01;34m\] \w \$\[\033[00m\] '     
else         
    PS1='\[\033[01;33m\]\u.\[\033[01;34m\]\[\033[01;32m\]\h\[\033[01;34m\] \ w \$\[\033[00m\] '     
    #PS1='\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] '     
fi     
alias ls='ls -G'     
alias grep='grep --colour=auto' else     if [[ ${EUID} == 0 ]] ; then         # show root@ when we don't have colors         PS1='\u@\h \W \$ '     else         PS1='\u@\h \w \$ '     fi fi # Try to keep environment pollution down, EPA loves us. unset use_color safe_term match_lhs