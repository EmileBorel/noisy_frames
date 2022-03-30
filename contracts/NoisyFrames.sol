//SPDX-License-Identifier: MIT
pragma solidity ^0.8.1;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "hardhat/console.sol";

// safeTransferFrom(from, to, tokenId, data)

contract NoisyFrames is ERC721, Ownable {
    uint MAX_FRAMES = 3333;
    string public baseURI;
    string public baseExtension = ".json";
    using Strings for uint256;

    constructor(
        string memory _name,
        string memory _symbol,
        string memory _initBaseURI,
        uint _owner_mintable

    ) ERC721(
            _name, _symbol
            ) 
    {
        baseURI = _initBaseURI;
        console.log(string(abi.encodePacked(
            "NoisyFrames Contract created with base uri: ", baseURI)
            ));

        while (_owner_mintable > 0) {
            mint(_owner_mintable);
            _owner_mintable--;
            }
    }


    // overloaded: mint specific token to specific adress
    function mint(uint256 tokenId) public payable {
            require(tokenId <= MAX_FRAMES, "TokenIds range from 0 to 3333");
            _safeMint(msg.sender, tokenId);
            console.log("An NFT w/ ID %s has been minted to %s", tokenId, msg.sender);
        }

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
            require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
            return bytes(baseURI).length > 0 ? string(
                abi.encodePacked(baseURI, tokenId.toString(), baseExtension)) : "";
        }

    function withdraw() public payable onlyOwner {
        (bool os, ) = payable(owner()).call{value: address(this).balance}("");
        require(os);
    }

}