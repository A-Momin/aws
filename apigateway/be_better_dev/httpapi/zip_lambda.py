import os
import shutil
import subprocess
import zipfile
from pathlib import Path

def zip_lambda_module_to_zip_file(module_name, module_dir, output_filename, requirements_file=None):
    """
    Zips a Python module as an AWS Lambda handler.

    :param module_name: The name of the Python module to include.
    :param module_dir: The directory containing the Python module.
    :param output_filename: The name of the output zip file.
    :param requirements_file: Path to the requirements.txt file (optional).
    """
    # Create a temporary directory to assemble the lambda package
    temp_dir = Path("temp_lambda_package")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    # Copy the specified module to the temporary directory
    source_path = Path(module_dir) / module_name
    destination_path = temp_dir / module_name

    if source_path.is_dir():
        shutil.copytree(source_path, destination_path)
    else:
        shutil.copy2(source_path, destination_path)

    # Install the dependencies if requirements_file is provided
    if requirements_file:
        subprocess.check_call([
            "pip", "install", "-r", requirements_file, 
            "-t", str(temp_dir)
        ])

    # Create the zip file
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                zipf.write(file_path, file_path.relative_to(temp_dir))

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

    print(f"Lambda function packaged as {output_filename}")

# Example usage
zip_lambda_module_to_zip_file(
    'httpapi_lambdahandler.py',
    '/Users/am/mydocs/Software_Development/Web_Development/aws/APIGateway/be_better_dev/httpapi',
    'lambdahandler.zip', 
    'requirements.txt'
)
