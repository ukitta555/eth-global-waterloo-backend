// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts@4.9.2/security/Pausable.sol";
import "@openzeppelin/contracts@4.9.2/access/Ownable.sol";
import "./library/SafeMath.sol";
import "./library/ABDKMathQuad.sol";

contract Core is Pausable, Ownable {
    using SafeMath for uint;
    using ABDKMathQuad for uint;
    using ABDKMathQuad for bytes16;
    struct raterInfo {
        uint lastBlock;
        uint balance;
    }

    struct ratedInfo {
        uint lastBlock;
        uint lastRating;
    }
    constructor() {
        mintUser(msg.sender, 100, 0);
    }
    mapping (address => raterInfo) public rater;
    mapping(address => ratedInfo) public rated;
    mapping (address => uint) public ratingGiven;
    event userMinted(address indexed user, uint amount, uint currentRepu);
    event ReputationMinted(address indexed user, uint amount);
    event Reputationtransferred(address indexed from, address indexed to, uint amount);
    function mintUser(address user, uint amount, uint currentRep) public onlyOwner(){
        require(rater[user].lastBlock == 0, "user already minted");
        require(amount != 0, "zero mint not allowed");
        raterInfo memory info = raterInfo(block.number, amount);
        rater[user] = info;
        if(currentRep != 0){
            rated[user] = ratedInfo(block.number, currentRep);
        }
        emit userMinted(user, amount, currentRep);
    }
    function mintReputation() public {
        uint prevBlock = rater[msg.sender].lastBlock;
        require(prevBlock != 0, "user does not exist");
        require(prevBlock != block.number, "please wait until next mint");
        uint prevRep = rater[msg.sender].balance;
        uint repNum = (block.number.sub(prevBlock)).mul(uint(10).add(uint256(keccak256(abi.encodePacked(block.timestamp)))%10));
        uint repDelta = repNum / 1 ; // otherwise should be 1 day or 7114 blocks
        uint rep = prevRep.add(repDelta);
        raterInfo memory info = raterInfo(block.number, rep);
        rater[msg.sender] = info;
        emit ReputationMinted(msg.sender, repDelta);
    }
    function transferReputation(address to, uint amount) public {
        require(rater[msg.sender].balance >= amount, "insufficient balance");
        require(to != msg.sender, "self attestation not allowed");
        require(rater[to].lastBlock != 0 || to == address(0), "recevier does not exist");
        raterInfo memory prevInfo = rater[msg.sender];
        raterInfo memory newRaterInfo = raterInfo(prevInfo.lastBlock, prevInfo.balance.sub(amount));
        rater[msg.sender] = newRaterInfo;
        ratingGiven[msg.sender] = ratingGiven[msg.sender].add(amount);
        if(to != address(0)){
          uint blockDelta = block.number.sub(rated[to].lastBlock);
          uint newRatingDecay = rated[to].lastRating.fromUInt().div(blockDelta.fromUInt().div(uint(5).fromUInt()).pow_2()).toUInt(); // half life otherwise is 50000 blocks
          uint newRating = amount.add(newRatingDecay);
          ratedInfo memory RatedInfo = ratedInfo(block.number, newRating);
          rated[to] = RatedInfo;
          emit Reputationtransferred(msg.sender, to, amount);
        }

    }

    function peekReputation(address user) public view returns (uint){
        require(rater[user].lastBlock != 0, "recevier does not exist");
        return rated[user].lastRating.fromUInt().div(block.number.sub(rated[user].lastBlock).fromUInt().div(uint(5).fromUInt()).pow_2()).toUInt(); // half life otherwise is 50000 blocks
    }
    function peekBalance(address user) public view returns (uint){
        require(rater[user].lastBlock != 0);
        return rater[user].balance;
    }
    function peekratings(address user) public view returns (uint){
        require(rater[user].lastBlock != 0);
        return ratingGiven[user];
    }
    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }
}