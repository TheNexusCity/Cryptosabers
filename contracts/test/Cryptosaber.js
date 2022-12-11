const { expect } = require('chai');

describe('Cryptosabers Contract Tests', async function () {
    let owner, addr1, addr2;
    let Cryptosabers, cryptosabers;
    let price;
    it('Deployment', async function () {
        [owner, addr1, addr2] = await ethers.getSigners();
        Cryptosabers = await ethers.getContractFactory('Cryptosabers');

        cryptosabers = await Cryptosabers.deploy(owner.address);

        await cryptosabers.deployed(owner.address);

        expect(await cryptosabers.totalSupply()).to.equal(0);

        const balance = await cryptosabers.balanceOf(owner.address);

        expect(balance).to.equal(0);
    });

    it('should deploy the contract', async function () {
        expect(cryptosabers.address).to.exist;
    });
    it('supports ERC165', async function () {
        expect(await cryptosabers.supportsInterface('0x01ffc9a7')).to.eq(true);
    });

    it('supports IERC721', async function () {
        expect(await cryptosabers.supportsInterface('0x80ac58cd')).to.eq(true);
    });

    it('supports ERC721Metadata', async function () {
        expect(await cryptosabers.supportsInterface('0x5b5e139f')).to.eq(true);
    });

    it('does not support random interface', async function () {
        expect(await cryptosabers.supportsInterface('0x00000042')).to.eq(false);
    });

    it('Mint cryptosaber for own address', async function () {
        Cryptosabers = await ethers.getContractFactory('Cryptosabers');

        cryptosabers = await Cryptosabers.deploy(owner.address);

        await cryptosabers.deployed(owner.address);

        expect(await cryptosabers.totalSupply()).to.equal(0);

        await cryptosabers.balanceOf(owner.address);

        // price is in wei
        price = await cryptosabers.getMintPrice();

        console.log('price', price);


        await cryptosabers.connect(addr1).mint(1, {
            value: price,
        });
    });

    it('Total supply should increase 1', async function () {
        expect(await cryptosabers.totalSupply()).to.equal(1);
    });

    it('Mint cryptosaber for treasury address', async function () {
        const price = await cryptosabers.getMintPrice();
        await cryptosabers.connect(addr1).mintForAddress(1, addr2.address, { value: price });
        const tknBal = await cryptosabers.balanceOf(addr2.address);
        expect(tknBal).to.equal(1);
    });

    it('Total supply should increase 2', async function () {
        expect(await cryptosabers.totalSupply()).to.equal(2);
    });

    it('Should transfer from owner to other address', async function () {
        let tknBal = await cryptosabers.balanceOf(addr1.address);
        console.log('tknBal', tknBal);
        const ownerOf0 = await cryptosabers.ownerOf(0);
        console.log('ownerOf0', ownerOf0);
        console.log('addr1.address', addr1.address);
        await cryptosabers.connect(addr1).transferFrom(addr1.address, addr2.address, 0);
        tknBal = await cryptosabers.balanceOf(addr1.address);
        expect(tknBal).to.equal(0);
    });

    it('Should transfer from treasury to other address', async function () {
        await cryptosabers.connect(addr2).transferFrom(addr2.address, addr1.address, 1);
        const tknBal = await cryptosabers.balanceOf(addr2.address);
        expect(tknBal).to.equal(1);
    });

    it('Owner should approve other account to transfer NFT', async function () {
        await cryptosabers.connect(addr1).approve(addr2.address, 1);
        expect(await cryptosabers.getApproved(1)).to.equal(addr2.address);
    });

    it('Other address should transfer cryptosaber', async function () {
        await cryptosabers.connect(addr2).transferFrom(addr1.address, addr2.address, 1);
        const tknBal = await cryptosabers.balanceOf(addr2.address);
        expect(tknBal).to.equal(2);
    });

    it('Owner should set the contract to be mintable for everybody ', async function () {
        let price = await cryptosabers.getMintPrice();
        await cryptosabers.connect(addr1)["mint(uint256)"](1, {
            value: price,
        });

        const tknBal = await cryptosabers.balanceOf(addr1.address);
        expect(tknBal).to.equal(1);
    });

    it('Total supply should increase', async function () {
        expect(await cryptosabers.totalSupply()).to.equal(3);
    });
});