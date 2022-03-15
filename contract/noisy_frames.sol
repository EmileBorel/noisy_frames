//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

// safeTransferFrom(from, to, tokenId, data)

contract NoisyFrames is ERC721, Ownable {
    uint OWNER_MINTABLE = 33;
    uint MAX_FRAMES = 3333; // ids start at 0 so 3333 unique frames
    string public baseURI;
    string public baseExtension = ".json";
    using Strings for uint256;


    constructor(
        string memory _name,
        string memory _symbol,
        string memory _initBaseURI

    ) ERC721(
            _name, _symbol
            ) 
    {
        baseURI = _initBaseURI;
        uint i = 1;
        while (i <= OWNER_MINTABLE) {
            mint(msg.sender, i);
            i++;
            }
    }


    function mint(address _to, uint256 tokenId) public payable {
            require(tokenId <= MAX_FRAMES, "TokenIds range from 0 to 3333");
            _safeMint(_to, tokenId);
            
        }


    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
            require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");

            return bytes(baseURI).length > 0 ? string(abi.encodePacked(baseURI, tokenId.toString(), baseExtension)) : "";
        }

    function withdraw() public payable onlyOwner {
        (bool os, ) = payable(owner()).call{value: address(this).balance}("");
        require(os);
    }

}