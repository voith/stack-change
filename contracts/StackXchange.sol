pragma solidity ^0.4.18;

contract Ownable {
  address public owner;

  function Ownable() {
    owner = msg.sender;
  }

  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }

  function transferOwnership(address _newOwner) onlyOwner {
    require(_newOwner != address(0));
    owner = _newOwner;
  }
}

contract StackXchange is Ownable {
  address owner;

  event emitDeposit(string indexed accountId, uint256 _amt);
  event emitWithdrawn(string indexed accountId, uint256 _amt);
  event emitFailWithdraw(string indexed accountId, uint256 _amt);

  function stackXchange() {
  }

  function deposit(string _accountId) public payable {
    emitDeposit(_accountId, msg.value);
  }

  function withDraw(address _address, string _accountId, uint256 _amt) public onlyOwner {
    if (_address.send(_amt)) {
        emitWithdrawn(_accountId, _amt);
    } else {
        emitFailWithdraw(_accountId, _amt);
    }
  }
}
