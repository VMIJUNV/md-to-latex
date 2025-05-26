import yaml

with open('Tool/config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    image=config['rule']['image']
    print(image)
    ...