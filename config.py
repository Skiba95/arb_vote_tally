rpc = "https://1rpc.io/arb"

random_wallets = False # Рандомизация кошельков True/False
random_enabled = True # Рандомный выбор варианта голосования True/False

# Treasury Governor - 0x789fc99093b09ad01c34dc7251d0c89ce743e5a4
# Core Governor - 0xf07DeD9dC292157749B6Fd268E37DF6EA38395B9

contract_address = "0xf07DeD9dC292157749B6Fd268E37DF6EA38395B9" # Адресс контракта, Treasury Governor или Core Governor 
proposal_id = 46905320292877192134536823079608810426433248493109520384601548724615383601450  # id proposal (https://www.tally.xyz/gov/arbitrum/proposal/110767177349707239820875764565747830009768307680609166467172874966002003291288)
support = 0  # 1 для "For", 2 для "Abstain", 0 для "Against"


delay_between_votes = 30

gas = 800000