from terminal import Color

class Messages:
    @staticmethod
    def ok(name):
        print(Color.OKGREEN + "+ Added \"" + name + "\"" + Color.ENDC)


    @staticmethod
    def conflict(name):
        print(Color.WARNING + "! \"" + name + "\" already present." + Color.ENDC)