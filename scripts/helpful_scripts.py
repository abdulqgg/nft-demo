from brownie import accounts, network, config, LinkToken, VRFCoordinatorMock, Contract

forked_local_enviroment = ["mainnet-fork-dev"]
local_blockchain_env = ["development", "ganache-local"]
opensea_url = "https://testnets.opensea.io/assets/{}/{}"

def get_account(index=None, id=None):
    # account[0]
    # accounts.add('env')
    # accounts.load('id')
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in local_blockchain_env
        or network.show_active() in forked_local_enviroment
    ):
        return accounts[0]
    
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}

def get_contract(contract_name):
    """ This function will grab teh contract address from
    the brownie config if defined, otherwise deploy a mack version of that contract, and return
    that mock contract.
    """
    contract_type = contract_to_mock[contract_name]

    if network.show_active() in local_blockchain_env:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(contract_type._name, contract_address,contract_type.abi)
    return contract

Decimals = 8
InitialValue = 250000000000

def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying Mock LinkToken...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("All done!")