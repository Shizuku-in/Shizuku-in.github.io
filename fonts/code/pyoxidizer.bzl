def make_python_packaging(ctx):
    # Define how the Python interpreter is embedded
    packaging = default_python_packaging()

    # Only include the necessary modules to minimize size
    packaging.default_modules = [
        "os", "tkinter", "PIL", "fontTools", "subprocess", "threading", "messagebox"
    ]

    # Add resource files if necessary
    packaging.add_python_resource(
        source_path=r"D:\Tools\hexo\source\fonts\code\utilities.py",  # Entry point for your program
        resource_name="utilities.py"
    )

    # Set the python entry point
    packaging.set_python_exe_resource("utilities.py")

    # Enable resource compression to save space
    packaging.add_compression_to_resources()

    # This will embed the Python interpreter and necessary packages
    return packaging
