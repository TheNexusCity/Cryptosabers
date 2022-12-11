pragma solidity ^0.8.4;

import "../node_modules/erc721a/contracts/ERC721A.sol";
import "../node_modules/@openzeppelin/contracts/utils/Address.sol";
import "../node_modules/@openzeppelin/contracts/utils/Strings.sol";
import "../node_modules/@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "../node_modules/@openzeppelin/contracts/access/Ownable.sol";

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
    string private _notRevealedUri = "";
    string private baseURI = "";
    string private _uriSuffix = ".json";
    uint256 private _whitelistPrice = 0.05 ether;
    uint256 private _basePrice = 0.088 ether;

    uint256 public maxSupply = 8888;
    uint256 royaltyPercentage = 10;
    bool public mintIsOpen = false;
    bool public revealed = false;

    constructor(address treasuryAddress)
        ERC721A("Cryptosabers", "CRYPTOSABERS")
    {
        _treasuryAddress = treasuryAddress;
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return baseURI;
    }

    function setRevealed(bool reveal) public onlyOwner {
        revealed = reveal;
    }

    function setNotRevealedUri(string memory notRevealedURI) public onlyOwner {
        _notRevealedUri = notRevealedURI;
    }

    function setBaseURI(string memory newBaseUri) public onlyOwner {
        baseURI = newBaseUri;
    }

    // function withdraw() public onlyOwner {
    //     _withdraw();
    // }

    function _withdraw() internal {
        (bool os, ) = payable(_treasuryAddress).call{
            value: address(this).balance
        }("");
        require(os);
    }

    function setOpenMint(bool open) public onlyOwner {
        mintIsOpen = open;
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
        if (mintIsOpen) {
            return _basePrice;
        } else {
            return _whitelistPrice;
        }
    }

    function setBasePrice(uint256 basePrice) public onlyOwner {
        _basePrice = basePrice;
    }

    function setWhitelistPrice(uint256 whitelistPrice) public onlyOwner {
        _whitelistPrice = whitelistPrice;
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
        _prepareMint(msg.sender, quantity, false); // whitelisted = false
    }

    function mintForAddress(uint256 quantity, address to) public payable {
        _prepareMint(to, quantity, false); // whitelisted = false
    }

    function mintWhiteList(uint256 quantity, bytes memory signature)
        public
        payable
    {
        bytes32 messagehash = keccak256(
            abi.encodePacked(address(this), owner(), msg.sender)
        );
        address signer = messagehash.toEthSignedMessageHash().recover(
            signature
        );
        _prepareMint(msg.sender, quantity, owner() == signer);
    }

    function _prepareMint(
        address to,
        uint256 quantity,
        bool whitelisted
    ) internal {
        require(
            owner() == msg.sender || mintIsOpen,
            "Minting is currently closed"
        ); // Don't allow anyone to mint if the mint is closed
        require(to != address(0), "Cannot send to 0x0"); // mint to the 0x0 address
        require(
            msg.value >=
                (whitelisted ? _whitelistPrice : _basePrice) * quantity,
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
