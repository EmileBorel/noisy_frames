const main = async () => {
    const nftContractFactory = await hre.ethers.getContractFactory('NoisyFrames');
    const nftContract = await nftContractFactory.deploy(
        'NoisyFrames', '~', 'ipfs://QmSHsVLkLhbXFmdHsc39BaAixtaJ9AGNCoBerxstpGtEea/', 33
    );
    await nftContract.deployed();
    console.log("Contract deployed to:", nftContract.address);
  
    // Call the function.
    let txn = await nftContract.mint(337)
    // Wait for it to be mined.
    await txn.wait()

  };
  
  const runMain = async () => {
    try {
      await main();
      process.exit(0);
    } catch (error) {
      console.log(error);
      process.exit(1);
    }
  };
  
  runMain();