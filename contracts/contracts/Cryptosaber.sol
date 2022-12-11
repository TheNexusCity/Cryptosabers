pragma solidity ^0.8.4;

import "erc721a/contracts/ERC721A.sol";
import "@openzeppelin/contracts/utils/Address.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface IERC2981Royalties {
    function royaltyInfo(uint256 _tokenId, uint256 _value)
        external
        view
        returns (address _receiver, uint256 _royaltyAmount);
}

contract Cryptosabers is ERC721A, IERC2981Royalties, Ownable {
    using Address for address;
    using Strings for uint256;
    using ECDSA for bytes32;

    address _treasuryAddress;
    string private baseURI = "";
    string private _uriSuffix = ".json";
    uint256 private _price = 0.088 ether;

    uint256 public maxSupply = 8888;
    uint256 royaltyPercentage = 1;

    constructor(address treasuryAddress)
        ERC721A("Cryptosabers", "CRYPTOSABERS")
    {
        _treasuryAddress = treasuryAddress;
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return baseURI;
    }

    function setBaseURI(string memory newBaseUri) public onlyOwner {
        baseURI = newBaseUri;
    }

    function _withdraw() internal {
        (bool os, ) = payable(_treasuryAddress).call{
            value: address(this).balance
        }("");
        require(os);
    }

    function royaltyInfo(uint256, uint256 value)
        external
        view
        override
        returns (address receiver, uint256 royaltyAmount)
    {
        return (_treasuryAddress, value * (royaltyPercentage / 100));
    }

    function setTreasuryAddres(address treasuryAddress) public onlyOwner {
        _treasuryAddress = treasuryAddress;
    }

    function getMintPrice() public view returns (uint256) {
            return _price;
    }

    function setBasePrice(uint256 basePrice) public onlyOwner {
        _price = basePrice;
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override
        returns (bool)
    {
        return
            interfaceId == type(IERC2981Royalties).interfaceId ||
            super.supportsInterface(interfaceId);
    }

    function mint(uint256 quantity) public payable {
        _prepareMint(msg.sender, quantity);
    }

    function mintForAddress(uint256 quantity, address to) public payable {
        _prepareMint(to, quantity);
    }

    function _prepareMint(
        address to,
        uint256 quantity
    ) internal {
        require(to != address(0), "Cannot send to 0x0"); // mint to the 0x0 address
        require(
            msg.value >= _price * quantity,
            "Insufficient funds!"
        );
        require(_nextTokenId() <= maxSupply, "No Cryptosabers left!"); // sold out
        require(
            _nextTokenId() + quantity <= maxSupply,
            "Not enough Cryptosabers left!"
        ); // cannot mint more than maxIndex tokens

        _mint(to, quantity);

        _withdraw();
    }
}
