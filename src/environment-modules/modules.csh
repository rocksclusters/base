if ($?tcsh) then
	set modules_shell="tcsh"
else
	set modules_shell="csh"
endif
set exec_prefix='/usr/bin'

set prefix=""
set postfix=""

if ( $?histchars ) then
  set histchar = `echo $histchars | cut -c1`
  set _histchars = $histchars

  set prefix  = 'unset histchars;'
  set postfix = 'set histchars = $_histchars;'
else
  set histchar = \!
endif

if ($?prompt) then
  set prefix  = "$prefix"'set _prompt="$prompt";set prompt="";'
  set postfix = "$postfix"'set prompt="$_prompt";unset _prompt;'
endif

if ($?noglob) then
  set prefix  = "$prefix""set noglob;"
  set postfix = "$postfix""unset noglob;"
endif
set postfix = "set _exit="'$status'"; $postfix; test 0 = "'$_exit;'

alias module $prefix'eval `'$exec_prefix'/modulecmd '$modules_shell' '$histchar'*`; '$postfix
unset exec_prefix
unset prefix
unset postfix

setenv MODULESHOME /usr/share/Modules

if (! $?MODULEPATH ) then
  setenv MODULEPATH `sed -n 's/[ 	#].*$//; /./H; $ { x; s/^\n//; s/\n/:/g; p; }' ${MODULESHOME}/init/.modulespath`
endif

if (! $?LOADEDMODULES ) then
  setenv LOADEDMODULES ""
endif
