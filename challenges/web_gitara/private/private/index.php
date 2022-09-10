<?php

if (!isset($_POST['domain']) || preg_match('/[^a-z0-9.-]/ims', $_POST['domain']) !== 0) {
	highlight_file(__FILE__);
} else {
	$dir = '/tmp/gitara'.rand();
	mkdir($dir);
	system(" \
cd $dir && \
timeout 2s sshpass -phunter2 scp -o StrictHostKeyChecking=no 'justctf-gitara@$_POST[domain]:*' . && \
timeout 1m git status; \
rm -rf $dir");
}
