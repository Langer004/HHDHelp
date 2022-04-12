pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol"; 

contract HypeDiscoNFT is ERC721, VRFConsumerBase{

    bytes32 internal keyHash;
    uint256 public fee; 
    uint256 public tokenCounter;

    enum Hyena{VIP, GOLD, GENERAL}

    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public  requestIdToTokenURI;
    mapping(uint256 => Hyena) public tokenIdToHyena;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event RequestedHyena(bytes32 indexed requestId); 
    event ReturnedHyena(bytes32 indexed requestId, uint256 randomNumber);

    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash) public 
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("HypeHyenaDisco","HHD")
    {
        keyHash = _keyhash;
        fee = 0.1 * 10 ** 18; //0.1 LINK
        tokenCounter = 0;
    }

    function createHyena(string memory tokenURI)
    public returns (bytes32)
    {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender; 
        requestIdToTokenURI[requestId] = tokenURI;
        emit RequestedHyena(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override{
        address hyenaOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(hyenaOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);
        Hyena status = Hyena(randomNumber % 3);
        tokenIdToHyena[newItemId] = status;
        requestIdToTokenId[requestId] = newItemId; 
        tokenCounter = tokenCounter + 1; 
        emit ReturnedHyena(requestId, randomNumber);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}