import unittest
import logging
import subprocess

class CaesarCipherTests(unittest.TestCase):
    def test_equal_output(self):
        self.assertEqual(run_assembly("aaaaaa", "1"), "bbbbbb")
        self.assertEqual(run_assembly("aaaaaa", "2"), "cccccc")
        self.assertEqual(run_assembly("aaaaaa", "23"), "xxxxxx")
        self.assertEqual(run_assembly("ABCAdgobnjsdifw", "2"), "CDECfiqdplufkhy")
        self.assertEqual(run_assembly("PIDJN5@@@@)))))", "14"), "DWRXB5@@@@)))))")
        self.assertEqual(run_assembly("PIDJN5@@@@)))))", "26"), "PIDJN5@@@@)))))")
        self.assertEqual(run_assembly("((((((^^^^^^))))))", "21"), "((((((^^^^^^))))))")
        self.assertEqual(run_assembly("ZZZZZZZZZ", "0"), "ZZZZZZZZZ")
        self.assertEqual(run_assembly("ZZZZZZZZZ", "26"), "ZZZZZZZZZ")
        self.assertEqual(run_assembly("ZZZZZZZZZ", "25"), "YYYYYYYYY")
        self.assertEqual(run_assembly("ZZZZZZZZZ", "1"), "AAAAAAAAA")
        self.assertEqual(run_assembly("ZZZZZZaaaaBBFWERD@Aaasadfsadas", "25"), "YYYYYYzzzzAAEVDQC@Zzzrzcerzczr")
        self.assertEqual(run_assembly("ABCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC", "25"), "ZABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        self.assertEqual(run_assembly("oijgnhsdkjinfwkjlbfjklb23w", "9"), "xrspwqbmtsrwoftsukostuk23f")
        self.assertEqual(run_assembly("DasD@!%$!^$@%^@#VZDBGDVEWFEAGREWSFEW", "11"), "OldO@!%$!^$@%^@#GKOMROGPHQPLRCPHDQPH")
        

    def test_errors(self):
        self.assertEqual(run_assembly("aaaaaa", "27"), "Your upper Index is either too big or too small. Please choose one between 0 to 26")
        self.assertEqual(run_assembly("aaaaaa", "52"), "Your upper Index is either too big or too small. Please choose one between 0 to 26")
        self.assertEqual(run_assembly("aaaaaa", "-1"), "Your upper Index is either too big or too small. Please choose one between 0 to 26")
        self.assertEqual(run_assembly("aaaaaa", "-10"), "Your upper Index is either too big or too small. Please choose one between 0 to 26")
        self.assertEqual(run_assembly("aaaaaa", "-99"), "Your upper Index is either too big or too small. Please choose one between 0 to 26")
        self.assertEqual(run_assembly("aaaaaa", "9999"), "Your upper Index is either too big or too small. Please choose one between 0 to 26")
        self.assertEqual(run_assembly("aaaaaa", "a"), "Your upper Index is either too big or too small. Please choose one between 0 to 26")
        self.assertEqual(run_assembly("aaaaaa", "a1"), "Your upper Index is either too big or too small. Please choose one between 0 to 26")
        self.assertEqual(run_assembly("aaaaaa", "1", "1"), "Wrong amount of args")
        self.assertEqual(run_assembly("1"), "Wrong amount of args")
        self.assertEqual(run_assembly("3211"), "Wrong amount of args")
        self.assertEqual(run_assembly("3211", "2121", "2121"), "Wrong amount of args")
        self.assertEqual(run_assembly("aaaaaa"), "Wrong amount of args")

def run_assembly(*args):
    if len(args) == 3:
        output = subprocess.Popen(["./caesar_cipher", args[0], args[1], args[2]], stdout=subprocess.PIPE).communicate()[0]
    elif len(args) == 2:
        output = subprocess.Popen(["./caesar_cipher", args[0], args[1]], stdout=subprocess.PIPE).communicate()[0]
    else:
        output = subprocess.Popen(["./caesar_cipher", args[0]], stdout=subprocess.PIPE).communicate()[0]

    return output.decode("utf-8")[0:-1]

if __name__ == '__main__':
    unittest.main()