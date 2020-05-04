from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
import os

class GoogleguetzliConan(ConanFile):
    name = "google-guetzli"
    version = "1.0.1"
    license = "Apache-2.0"
    
    url = "https://github.com/google/guetzli"
    description = "Perceptual JPEG encoder"
    topics = ("jpeg")
    settings = "os", "compiler", "build_type", "arch"
    
    generators = "pkg_config"
    requires = ["libpng/1.6.37"]

    def configure(self):
        if self.settings.os not in ["Linux"]:
            raise ConanInvalidConfiguration("conan recipe for  google-guetzli v{0} is not \
                available in {1}.".format(self.version, self.settings.os))

    def source(self):
        self.run("git clone https://github.com/google/guetzli.git .")
        

    def build(self):
        print("build folder is {}".format(self.build_folder))
        with tools.chdir(self.build_folder):
            print("cwd = {}".format(os.getcwd()))
            with tools.environment_append({"PKG_CONFIG_PATH":self.build_folder}):
                self.run("make")
            
    def package(self):
        
        self.copy("bin/Release/guetzli", dst="bin", keep_path=False)
        self.copy("LICENSE",dst="licenses")
        

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)

