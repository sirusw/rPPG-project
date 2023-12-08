import sys
from procedure import *   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    run = Procedure()
    sys.exit(app.exec_())
