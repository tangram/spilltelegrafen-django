from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.datastructures import SortedDict
import hashlib

def mask_hash(hash, show=6, char="*"):
    """
    Returns the given hash, with only the first ``show`` number shown. The
    rest are masked with ``char`` for security reasons.
    """
    masked = hash[:show]
    masked += char * len(hash[show:])
    return masked

class PHPassHasher(BasePasswordHasher):
    """
    One-off password hash verification for PHPass internal MD5 hasher.
    Doesn't actually encrypt!
    Expects hashes to be stored as P$<hash> (no preceding $)
    """

    algorithm = 'P'
    itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    def encode64(self, inp, count):
        outp = ''
        cur = 0
        while cur < count:
            value = ord(inp[cur])
            cur += 1
            outp += self.itoa64[value & 0x3f]
            if cur < count:
                value |= (ord(inp[cur]) << 8)
            outp += self.itoa64[(value >> 6) & 0x3f]
            if cur >= count:
                break
            cur += 1
            if cur < count:
                value |= (ord(inp[cur]) << 16)
            outp += self.itoa64[(value >> 12) & 0x3f]
            if cur >= count:
                break
            cur += 1
            outp += self.itoa64[(value >> 18) & 0x3f]
        return outp
    
    def crypt_private(self, pw, setting):
        outp = '*0'
        count_log2 = self.itoa64.find(setting[2])
        if count_log2 < 7 or count_log2 > 30:
            return outp
        count = 1 << count_log2
        salt = setting[3:11]
        if len(salt) != 8:
            return outp
        if not isinstance(pw, str):
            pw = pw.encode('utf-8')
        hx = hashlib.md5(salt + pw).digest()
        while count:
            hx = hashlib.md5(hx + pw).digest()
            count -= 1
        return setting[:11] + self.encode64(hx, 16)
    
    def encode(self, password, salt):
        return ''
    
    def verify(self, password, encoded):
        return encoded == self.crypt_private(password, encoded)

    def safe_summary(self, encoded):
        algorithm, hash = encoded.split('$', 1)
        salt = encoded[4:12]
        assert algorithm == self.algorithm
        return SortedDict([
            (('algorithm'), algorithm),
            (('iterations'), 2 ** self.itoa64.index(self.iter_code)),
            (('salt'), mask_hash(salt)),
            (('hash'), mask_hash(hash)),
        ])