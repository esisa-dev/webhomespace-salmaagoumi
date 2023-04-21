import os, spwd, crypt, datetime, math

class UserDao:
    def _init_(self) -> None: 
        self.logged = False
        pass

    def authenticate(self, username, password) -> bool:
        user = spwd.getspnam(username)
        if crypt.crypt(password, user.sp_pwdp) == user.sp_pwdp:
            self.logged = True
            return True
        return False

    def __convertSize(self, size):
        if size < 1024:
            return '{} bytes'.format(size)
        elif size < 1048576:
            return '{:.1f} KB'.format(size / 1024)
        else:
            return '{:.1f} MB'.format(size / 1048576)

    def getUserData(self, path):
        dirs = []
        files = []
        if(self.logged):
            for data in os.listdir(path):
                datapath = f'{path}/{data}'
                size = os.path.getsize(datapath)
                size_str = self.__convertSize(size)
                mtime = os.path.getmtime(datapath)
                mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                datapath = f'{path}/{data}'
                if os.path.isdir(datapath):
                    dirs.append((data, mtime_str, size_str, datapath))
                if os.path.isfile(datapath):
                    files.append((data, mtime_str, size_str))
            return (dirs,files)
        return []
        
