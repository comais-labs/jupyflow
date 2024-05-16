import ansible_runner

from base.settings import BASE_DIR

def setup():
    runner = ansible_runner.run(
        playbook=f"{BASE_DIR}/ansible/playbook.yml", 
        extravars={"users":[{"password":"comais","user":"comais"},{"password":"rogerio","user":"rogerio"}]})
    print(runner.status)

if __name__=="__main__":
    setup()