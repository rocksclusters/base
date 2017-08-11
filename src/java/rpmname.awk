/^Name/ {name=$NF}
/^Version/ {version=$NF}
/^Release/ {release=$NF}
/^Architecture/	{arch=$NF}
END{printf("%s-%s-%s.%s.rpm",name,version,release,arch)}
