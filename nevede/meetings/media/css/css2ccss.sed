# usage: sed -f css2ccss.sed file.css
s/{/:/
s/}//
s/\ *:\ */: /
s/\;//
