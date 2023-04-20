import os, spwd, crypt

class UserDao:
  def _init_(self) -> None:
    f=open('/etc/shadow', 'r')
    self.data = f.readlines()
    f.close()

  def authenticate(self, username, password) -> bool:
    user = spwd.getspnam(username)
    return crypt.crypt(password, user.sp_pwdp) == user.sp_pwdp