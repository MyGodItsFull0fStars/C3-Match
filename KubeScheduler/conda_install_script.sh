echo "Starting the installation"

conda create -n scheduler python=3.9 -y
conda activate scheduler
conda install numpy -y
pip install prometheus-api-client -y
pip install kubernetes -y

echo "Success"
