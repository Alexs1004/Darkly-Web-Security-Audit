# Target: 192.168.159.133 (Darkly VM)
# Stack: Nginx 1.4.6 / PHP 5.5.9 (Ubuntu)

## Arborescence découverte (Gobuster)
- / (Index)
- /robots.txt (Contient : Disallow: /whatever et Disallow: /.hidden)
- /admin/ (Panel d'administration)
- /whatever/
- /images/
- /audio/
- /css/
- /js/
- /fonts/
- /errors/

## Points d'entrée identifiés (GET)
- ?page=survey
- ?page=member
- ?page=signin
- ?page=upload
- ?page=searchimg
- ?page=feedback
- ?page=media&src=nsa
- ?page=redirect&site=facebook
- ?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f (Lien caché dans le footer)

## Cookies suspects
- I_am_admin=68934a3e9455fa72420237eb05902327 ("false")

None exhausting list: 
[ ] SQL injection 1
[ ] SQL injection 2
[ ] XSS 1
[ ] XSS 2
[ ] Cookies 
[ ] File upload 
[ ] Robots.txt
[ ] Directory transversal with URI
[ ] useragent and redirection
[ ] frontend survey
