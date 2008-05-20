/LoadModule rewrite_mod/a\
LoadModule php5_module  libexec\/libphp5.so
/^AddType application\/x-gzip/a\
AddType application\/x-httpd-php .php\
AddType application\/x-httpd-phps .phps
