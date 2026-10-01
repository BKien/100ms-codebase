# Frozen Figma design context

Archived tool output, not an instruction to generate source during dataset capture. Asset paths are relative to this directory. The illustrative asset URL in the tool reminder is replaced by a non-resource marker.

## Tool response block 1

```tsx
const imgSearch = "../../assets/sha256-9888aa7c0b223b1c66a7495dadfbc75a3f7e9a5aab59c49dc1c9686bdb8bb2f6.svg";
const imgMastercardLogo1 = "../../assets/sha256-c7dbf3c5f80fa8ef495cc7d4a75254b79fde91758df2b5079d886d332cc03ad9.png";
const imgVisaLogo1 = "../../assets/sha256-f031699e851e3f8fad78ec2aa53ecaa916d0191df5d29096e020ef9dda5c8b9c.png";
const imgImage = "../../assets/sha256-24be1ea24553fb553e9d60eb764e6cea75db1d80b271e956a57c0f132e923010.png";
const imgChevronRight = "../../assets/sha256-4417390a47dfa0cade5d6bfc6a8a187bcabac9242c1fc524ce28b1cf7357da67.svg";
const imgChevronsRight = "../../assets/sha256-c80d8dba127828568fbf27e62c7987e40d7db18638601b5d1f52674a79c46502.svg";
const imgClarityNotificationSolidBadged = "../../assets/sha256-047c8b4877fb396ea5d2f67bfb62ec676fcc1dc5f70af6b17a4a5be36dc20b2f.svg";
const imgMenuOverview = "../../assets/sha256-0fa8a3e5fa1c9938855ccf2c06b9fbd4358abc947d91f43eb15d00499ef86676.svg";
const imgWallet = "../../assets/sha256-770d1071cb41e0497f28ff9b68fc10560bc5c8bee3292e3facb3f6fa884c7330.svg";
const imgTransaction = "../../assets/sha256-196148b4f7f85b838bbeb503a648df00b710a06014e46753d3a202f68986fff9.svg";
const imgBill = "../../assets/sha256-f4d81f00226c061da6e132978f4bc08749049dbcc5acb20aac2bff11a1b40045.svg";
const imgGroup = "../../assets/sha256-ac65a8241d3c5e56d6d598c64510f6c0e9463bdccd6e19f09d4a1e277048c5ba.svg";
const imgGoal = "../../assets/sha256-fa4544ddd18fa692c4b53eee145b1c10323b9b58470b41e8eaf23ff8162d56f0.svg";
const imgMenuSettings = "../../assets/sha256-78a004721cfe6674fd707999793f7033f336985bc101510f32d274e1b51302a2.svg";
const imgLogout = "../../assets/sha256-c690ae811c470d066d09b8e568d175e934a4c2f04a491f1f8b78e500f29d483c.svg";
const imgIcon = "../../assets/sha256-6dc81638c4dc26974ff2d1bff954a1384d188f85298f626452a7a49ba1d39f77.svg";

function Search({ className }: { className?: string }) {
  return (
    <div className={className || "relative size-[24px]"} data-node-id="54:2473" data-name="search">
      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgSearch} />
    </div>
  );
}

function Mastercard({ className }: { className?: string }) {
  return (
    <div className={className || "h-[32px] overflow-clip relative w-[48px]"} data-node-id="408:5979" data-name="Mastercard">
      <div className="absolute h-[24px] left-[3px] top-[4px] w-[43px]" data-node-id="408:5989" data-name="Mastercard-Logo 1">
        <img alt="" className="absolute inset-0 max-w-none object-cover pointer-events-none size-full" src={imgMastercardLogo1} />
      </div>
    </div>
  );
}

export default function Component105ViewBankAccounts() {
  return (
    <div className="bg-[#f4f5f7] relative size-full" data-node-id="66:5320" data-name="105. View Bank Accounts">
      <div className="absolute content-stretch flex flex-col gap-[16px] items-start left-[304px] top-[104px]" data-node-id="410:5547" data-name="Balances">
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[32px] not-italic relative shrink-0 text-[#878787] text-[22px] whitespace-nowrap" data-node-id="66:5347">
          Balances
        </p>
        <div className="content-stretch flex flex-col gap-[32px] items-start relative shrink-0" data-node-id="410:5546" data-name="Account Type">
          <div className="content-stretch flex gap-[24px] items-start relative shrink-0" data-node-id="410:5398" data-name="Top line">
            <div className="bg-white content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col gap-[16px] items-start p-[24px] relative rounded-[8px] shrink-0" data-node-id="410:5376" data-name="Account Type">
              <div className="border-[rgba(210,210,210,0.25)] border-b border-solid content-stretch flex h-[44px] items-center justify-between pb-[12px] relative shrink-0 w-[304px]" data-node-id="I410:5376;410:5321" data-name="Header">
                <p className="[word-break:break-word] capitalize font-['Inter:Bold'] font-bold leading-[24px] not-italic relative shrink-0 text-[#878787] text-[16px] whitespace-nowrap" data-node-id="I410:5376;410:5322">
                  Credit Card
                </p>
                <div className="content-stretch flex gap-[4px] items-center relative shrink-0" data-node-id="I410:5376;410:5351" data-name="Type">
                  <div className="content-stretch flex items-start py-[8px] relative shrink-0" data-node-id="I410:5376;410:5445">
                    <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[16px] not-italic relative shrink-0 text-[#666] text-[12px] text-right whitespace-nowrap" data-node-id="I410:5376;410:5350">
                      Master Card
                    </p>
                  </div>
                  <div className="content-stretch flex items-center relative shrink-0" data-node-id="I410:5376;410:5323" data-name="Icon">
                    <Mastercard className="h-[32px] overflow-clip relative shrink-0 w-[48px]" />
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0" data-node-id="I410:5376;410:5330" data-name="Content">
                <div className="[word-break:break-word] content-stretch flex flex-col gap-[16px] items-start not-italic relative shrink-0" data-node-id="I410:5376;410:5349" data-name="Account Details">
                  <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="I410:5376;410:5331" data-name="Account Number">
                    <p className="capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] relative shrink-0 text-[#191919] text-[20px] w-[304px] whitespace-pre-wrap" data-node-id="I410:5376;410:5332">{`3388 4556  8860 8***`}</p>
                    <p className="font-['Inter:Regular'] font-normal leading-[20px] relative shrink-0 text-[#9f9f9f] text-[14px] w-[128px]" data-node-id="I410:5376;410:5333">
                      Account Number
                    </p>
                  </div>
                  <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="I410:5376;410:5335" data-name="Total amount">
                    <p className="capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] relative shrink-0 text-[#191919] text-[20px] w-[125px]" data-node-id="I410:5376;410:5336">
                      $25000
                    </p>
                    <p className="font-['Inter:Regular'] font-normal leading-[20px] relative shrink-0 text-[#9f9f9f] text-[14px] w-[125px]" data-node-id="I410:5376;410:5337">
                      Total amount
                    </p>
                  </div>
                </div>
                <div className="content-stretch flex items-center justify-between relative shrink-0 w-[303px]" data-node-id="I410:5376;410:5338" data-name="Footer">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#299d91] text-[16px] w-[116px]" data-node-id="I410:5376;410:5340">
                    Remove
                  </p>
                  <a className="bg-[#299d91] content-stretch cursor-pointer flex gap-[8px] items-center px-[20px] py-[8px] relative rounded-[4px] shrink-0" data-node-id="I410:5376;410:5339" data-name="Button">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[14px] text-left text-white whitespace-nowrap" data-node-id="I410:5376;410:5339;36:1180">
                      Details
                    </p>
                    <div className="relative shrink-0 size-[16px]" data-node-id="I410:5376;410:5339;36:1181" data-name="chevron-right">
                      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronRight} />
                    </div>
                  </a>
                </div>
              </div>
            </div>
            <div className="bg-white content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col gap-[16px] items-start p-[24px] relative rounded-[8px] shrink-0" data-node-id="410:5354" data-name="Account Type">
              <div className="border-[rgba(210,210,210,0.25)] border-b border-solid content-stretch flex h-[44px] items-center justify-between pb-[12px] relative shrink-0 w-[304px]" data-node-id="I410:5354;410:5321" data-name="Header">
                <p className="[word-break:break-word] capitalize font-['Inter:Bold'] font-bold leading-[24px] not-italic relative shrink-0 text-[#878787] text-[16px] whitespace-nowrap" data-node-id="I410:5354;410:5322">
                  Checking
                </p>
                <div className="content-stretch flex gap-[4px] items-center relative shrink-0" data-node-id="I410:5354;410:5351" data-name="Type">
                  <div className="content-stretch flex items-start py-[8px] relative shrink-0" data-node-id="I410:5354;410:5445">
                    <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[16px] not-italic relative shrink-0 text-[#666] text-[12px] text-right whitespace-nowrap" data-node-id="I410:5354;410:5350">
                      AB Bank Ltd
                    </p>
                  </div>
                  <div className="content-stretch flex items-center relative shrink-0" data-node-id="I410:5354;410:5323" data-name="Icon">
                    <div className="h-[32px] overflow-clip relative shrink-0 w-[48px]" data-node-id="I410:5354;410:5347" data-name="Visacard">
                      <div className="absolute h-[14px] left-px top-[9px] w-[46px]" data-node-id="I410:5354;410:5347;410:5466" data-name="Visa_Logo 1">
                        <img alt="" className="absolute inset-0 max-w-none object-cover pointer-events-none size-full" src={imgVisaLogo1} />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0" data-node-id="I410:5354;410:5330" data-name="Content">
                <div className="[word-break:break-word] content-stretch flex flex-col gap-[16px] items-start not-italic relative shrink-0" data-node-id="I410:5354;410:5349" data-name="Account Details">
                  <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="I410:5354;410:5331" data-name="Account Number">
                    <p className="capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] relative shrink-0 text-[#191919] text-[20px] w-[304px] whitespace-pre-wrap" data-node-id="I410:5354;410:5332">{`693 456  69 9****`}</p>
                    <p className="font-['Inter:Regular'] font-normal leading-[20px] relative shrink-0 text-[#9f9f9f] text-[14px] w-[128px]" data-node-id="I410:5354;410:5333">
                      Account Number
                    </p>
                  </div>
                  <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="I410:5354;410:5335" data-name="Total amount">
                    <p className="capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] relative shrink-0 text-[#191919] text-[20px] w-[125px]" data-node-id="I410:5354;410:5336">
                      $25000
                    </p>
                    <p className="font-['Inter:Regular'] font-normal leading-[20px] relative shrink-0 text-[#9f9f9f] text-[14px] w-[125px]" data-node-id="I410:5354;410:5337">
                      Total amount
                    </p>
                  </div>
                </div>
                <div className="content-stretch flex items-center justify-between relative shrink-0 w-[303px]" data-node-id="I410:5354;410:5338" data-name="Footer">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#299d91] text-[16px] w-[116px]" data-node-id="I410:5354;410:5340">
                    Remove
                  </p>
                  <a className="bg-[#299d91] content-stretch cursor-pointer flex gap-[8px] items-center px-[20px] py-[8px] relative rounded-[4px] shrink-0" data-node-id="I410:5354;410:5339" data-name="Button">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[14px] text-left text-white whitespace-nowrap" data-node-id="I410:5354;410:5339;36:1180">
                      Details
                    </p>
                    <div className="relative shrink-0 size-[16px]" data-node-id="I410:5354;410:5339;36:1181" data-name="chevron-right">
                      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronRight} />
                    </div>
                  </a>
                </div>
              </div>
            </div>
            <div className="bg-white content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col gap-[16px] items-start p-[24px] relative rounded-[8px] shrink-0" data-node-id="410:5421" data-name="Account Type">
              <div className="border-[rgba(210,210,210,0.25)] border-b border-solid content-stretch flex h-[44px] items-center justify-between pb-[12px] relative shrink-0 w-[304px]" data-node-id="I410:5421;410:5321" data-name="Header">
                <p className="[word-break:break-word] capitalize font-['Inter:Bold'] font-bold leading-[24px] not-italic relative shrink-0 text-[#878787] text-[16px] whitespace-nowrap" data-node-id="I410:5421;410:5322">
                  savings
                </p>
                <div className="content-stretch flex gap-[4px] items-center relative shrink-0" data-node-id="I410:5421;410:5351" data-name="Type">
                  <div className="content-stretch flex items-start py-[8px] relative shrink-0" data-node-id="I410:5421;410:5445">
                    <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[16px] not-italic relative shrink-0 text-[#666] text-[12px] text-right whitespace-nowrap" data-node-id="I410:5421;410:5350">
                      Brac Bank Ltd.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0" data-node-id="I410:5421;410:5330" data-name="Content">
                <div className="[word-break:break-word] content-stretch flex flex-col gap-[16px] items-start not-italic relative shrink-0" data-node-id="I410:5421;410:5349" data-name="Account Details">
                  <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="I410:5421;410:5331" data-name="Account Number">
                    <p className="capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] relative shrink-0 text-[#191919] text-[20px] w-[304px] whitespace-pre-wrap" data-node-id="I410:5421;410:5332">{`133 456  886 8****`}</p>
                    <p className="font-['Inter:Regular'] font-normal leading-[20px] relative shrink-0 text-[#9f9f9f] text-[14px] w-[128px]" data-node-id="I410:5421;410:5333">
                      Account Number
                    </p>
                  </div>
                  <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="I410:5421;410:5335" data-name="Total amount">
                    <p className="capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] relative shrink-0 text-[#191919] text-[20px] w-[125px]" data-node-id="I410:5421;410:5336">
                      $25000
                    </p>
                    <p className="font-['Inter:Regular'] font-normal leading-[20px] relative shrink-0 text-[#9f9f9f] text-[14px] w-[125px]" data-node-id="I410:5421;410:5337">
                      Total amount
                    </p>
                  </div>
                </div>
                <div className="content-stretch flex items-center justify-between relative shrink-0 w-[303px]" data-node-id="I410:5421;410:5338" data-name="Footer">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#299d91] text-[16px] w-[116px]" data-node-id="I410:5421;410:5340">
                    Remove
                  </p>
                  <a className="bg-[#299d91] content-stretch cursor-pointer flex gap-[8px] items-center px-[20px] py-[8px] relative rounded-[4px] shrink-0" data-node-id="I410:5421;410:5339" data-name="Button">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[14px] text-left text-white whitespace-nowrap" data-node-id="I410:5421;410:5339;36:1180">
                      Details
                    </p>
                    <div className="relative shrink-0 size-[16px]" data-node-id="I410:5421;410:5339;36:1181" data-name="chevron-right">
                      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronRight} />
                    </div>
                  </a>
                </div>
              </div>
            </div>
          </div>
          <div className="content-stretch flex gap-[24px] items-start relative shrink-0" data-node-id="410:5515" data-name="Bottom Line">
            <div className="bg-white content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col gap-[16px] items-start p-[24px] relative rounded-[8px] shrink-0" data-node-id="410:5492" data-name="Account Type">
              <div className="border-[rgba(210,210,210,0.25)] border-b border-solid content-stretch flex h-[44px] items-center justify-between pb-[12px] relative shrink-0 w-[304px]" data-node-id="I410:5492;410:5321" data-name="Header">
                <p className="[word-break:break-word] capitalize font-['Inter:Bold'] font-bold leading-[24px] not-italic relative shrink-0 text-[#878787] text-[16px] whitespace-nowrap" data-node-id="I410:5492;410:5322">
                  Investment
                </p>
                <div className="content-stretch flex gap-[4px] items-center relative shrink-0" data-node-id="I410:5492;410:5351" data-name="Type">
                  <div className="content-stretch flex items-start py-[8px] relative shrink-0" data-node-id="I410:5492;410:5445">
                    <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[16px] not-italic relative shrink-0 text-[#666] text-[12px] text-right whitespace-nowrap" data-node-id="I410:5492;410:5350">
                      AB Bank Ltd
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0" data-node-id="I410:5492;410:5330" data-name="Content">
                <div className="[word-break:break-word] content-stretch flex flex-col gap-[16px] items-start not-italic relative shrink-0" data-node-id="I410:5492;410:5349" data-name="Account Details">
                  <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="I410:5492;410:5331" data-name="Account Number">
                    <p className="capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] relative shrink-0 text-[#191919] text-[20px] w-[304px] whitespace-pre-wrap" data-node-id="I410:5492;410:5332">{`698 456  866 2****`}</p>
                    <p className="font-['Inter:Regular'] font-normal leading-[20px] relative shrink-0 text-[#9f9f9f] text-[14px] w-[128px]" data-node-id="I410:5492;410:5333">
                      Account Number
                    </p>
                  </div>
                  <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="I410:5492;410:5335" data-name="Total amount">
                    <p className="capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] relative shrink-0 text-[#191919] text-[20px] w-[125px]" data-node-id="I410:5492;410:5336">
                      $25000
                    </p>
                    <p className="font-['Inter:Regular'] font-normal leading-[20px] relative shrink-0 text-[#9f9f9f] text-[14px] w-[125px]" data-node-id="I410:5492;410:5337">
                      Total amount
                    </p>
                  </div>
                </div>
                <div className="content-stretch flex items-center justify-between relative shrink-0 w-[303px]" data-node-id="I410:5492;410:5338" data-name="Footer">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#299d91] text-[16px] w-[116px]" data-node-id="I410:5492;410:5340">
                    Remove
                  </p>
                  <a className="bg-[#299d91] content-stretch cursor-pointer flex gap-[8px] items-center px-[20px] py-[8px] relative rounded-[4px] shrink-0" data-node-id="I410:5492;410:5339" data-name="Button">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[14px] text-left text-white whitespace-nowrap" data-node-id="I410:5492;410:5339;36:1180">
                      Details
                    </p>
                    <div className="relative shrink-0 size-[16px]" data-node-id="I410:5492;410:5339;36:1181" data-name="chevron-right">
                      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronRight} />
                    </div>
                  </a>
                </div>
              </div>
            </div>
            <div className="bg-white content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col gap-[16px] items-start p-[24px] relative rounded-[8px] shrink-0" data-node-id="410:5469" data-name="Account Type">
              <div className="border-[rgba(210,210,210,0.25)] border-b border-solid content-stretch flex h-[44px] items-center justify-between pb-[12px] relative shrink-0 w-[304px]" data-node-id="I410:5469;410:5321" data-name="Header">
                <p className="[word-break:break-word] capitalize font-['Inter:Bold'] font-bold leading-[24px] not-italic relative shrink-0 text-[#878787] text-[16px] whitespace-nowrap" data-node-id="I410:5469;410:5322">
                  Loan
                </p>
                <div className="content-stretch flex gap-[4px] items-center relative shrink-0" data-node-id="I410:5469;410:5351" data-name="Type">
                  <div className="content-stretch flex items-start py-[8px] relative shrink-0" data-node-id="I410:5469;410:5445">
                    <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[16px] not-italic relative shrink-0 text-[#666] text-[12px] text-right whitespace-nowrap" data-node-id="I410:5469;410:5350">
                      City Bank Ltd.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0" data-node-id="I410:5469;410:5330" data-name="Content">
                <div className="[word-break:break-word] content-stretch flex flex-col gap-[16px] items-start not-italic relative shrink-0" data-node-id="I410:5469;410:5349" data-name="Account Details">
                  <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="I410:5469;410:5331" data-name="Account Number">
                    <p className="capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] relative shrink-0 text-[#191919] text-[20px] w-[304px] whitespace-pre-wrap" data-node-id="I410:5469;410:5332">{`363 456  896 6****`}</p>
                    <p className="font-['Inter:Regular'] font-normal leading-[20px] relative shrink-0 text-[#9f9f9f] text-[14px] w-[128px]" data-node-id="I410:5469;410:5333">
                      Account Number
                    </p>
                  </div>
                  <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="I410:5469;410:5335" data-name="Total amount">
                    <p className="capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] relative shrink-0 text-[#191919] text-[20px] w-[125px]" data-node-id="I410:5469;410:5336">
                      $25000
                    </p>
                    <p className="font-['Inter:Regular'] font-normal leading-[20px] relative shrink-0 text-[#9f9f9f] text-[14px] w-[125px]" data-node-id="I410:5469;410:5337">
                      Total amount
                    </p>
                  </div>
                </div>
                <div className="content-stretch flex items-center justify-between relative shrink-0 w-[303px]" data-node-id="I410:5469;410:5338" data-name="Footer">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#299d91] text-[16px] w-[116px]" data-node-id="I410:5469;410:5340">
                    Remove
                  </p>
                  <a className="bg-[#299d91] content-stretch cursor-pointer flex gap-[8px] items-center px-[20px] py-[8px] relative rounded-[4px] shrink-0" data-node-id="I410:5469;410:5339" data-name="Button">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[14px] text-left text-white whitespace-nowrap" data-node-id="I410:5469;410:5339;36:1180">
                      Details
                    </p>
                    <div className="relative shrink-0 size-[16px]" data-node-id="I410:5469;410:5339;36:1181" data-name="chevron-right">
                      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronRight} />
                    </div>
                  </a>
                </div>
              </div>
            </div>
            <div className="bg-white content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col items-center justify-center pb-[88px] pt-[100px] px-[24px] relative rounded-[8px] shrink-0 w-[352px]" data-node-id="410:5516" data-name="Add Account">
              <div className="content-stretch flex flex-col gap-[4px] items-start relative shrink-0" data-node-id="410:5517" data-name="Button">
                <div className="bg-[#299d91] content-stretch flex items-center px-[32px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="410:5539" data-name="Button Big">
                  <p className="[word-break:break-word] capitalize font-['Inter:Bold'] font-bold leading-[24px] not-italic relative shrink-0 text-[16px] text-center text-white w-[144px]" data-node-id="I410:5539;410:5535">
                    Add accounts
                  </p>
                </div>
                <div className="content-stretch flex items-start px-[24px] py-[12px] relative shrink-0" data-node-id="410:5545">
                  <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[24px] not-italic relative shrink-0 text-[#9f9f9f] text-[16px] text-center w-[160px]" data-node-id="410:5530">
                    Edit Accounts
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="absolute border-[#e8e8e8] border-b border-solid content-stretch flex items-center justify-between left-[280px] pl-[24px] pr-[32px] py-[20px] top-0 w-[1160px]" data-node-id="411:6111" data-name="Header">
        <div className="content-stretch flex gap-[24px] items-center relative shrink-0" data-node-id="I411:6111;411:6047" data-name="Header">
          <div className="content-stretch flex gap-[4px] items-center relative shrink-0" data-node-id="I411:6111;411:6049" data-name="Date">
            <div className="relative shrink-0 size-[24px]" data-node-id="I411:6111;411:6050" data-name="chevrons-right">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronsRight} />
            </div>
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[#9f9f9f] text-[14px] whitespace-nowrap" data-node-id="I411:6111;411:6053">
              May 19, 2023
            </p>
          </div>
        </div>
        <div className="content-stretch flex gap-[40px] items-center relative shrink-0" data-node-id="I411:6111;411:6054" data-name="Search">
          <div className="content-stretch flex items-center relative shrink-0" data-node-id="I411:6111;411:6055" data-name="Notification icon">
            <div className="grid-cols-[max-content] grid-rows-[max-content] inline-grid leading-[0] place-items-start relative shrink-0" data-node-id="I411:6111;411:6055;2:622">
              <div className="col-1 ml-0 mt-0 relative row-1 size-[24px]" data-node-id="I411:6111;411:6055;2:623" data-name="clarity:notification-solid-badged">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgClarityNotificationSolidBadged} />
              </div>
            </div>
          </div>
          <div className="bg-white content-stretch drop-shadow-[0px_26px_13px_rgba(106,22,58,0.04)] flex gap-[170px] items-start pl-[32px] pr-[24px] py-[12px] relative rounded-[12px] shrink-0" data-node-id="I411:6111;411:6056" data-name="Search">
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#9f9f9f] text-[16px] w-[102px]" data-node-id="I411:6111;411:6056;404:5259">
              Search here
            </p>
            <Search className="relative shrink-0 size-[24px]" />
          </div>
        </div>
      </div>
      <div className="absolute bg-[#191919] content-stretch flex flex-col gap-[228px] items-start left-0 px-[28px] py-[48px] top-0" data-node-id="413:7727" data-name="Nav bar">
        <div className="content-stretch flex flex-col gap-[40px] items-start relative shrink-0" data-node-id="I413:7727;411:6376" data-name="Logo & Menu">
          <a className="[word-break:break-word] block cursor-pointer font-['Poppins:Bold'] leading-[0] not-italic relative shrink-0 text-[0px] text-center text-white tracking-[1.92px] w-[224px]" data-node-id="I413:7727;411:6377">
            <p className="text-[24px]">
              <span className="font-['Poppins:ExtraBold'] leading-[32px]">FINE</span>
              <span className="font-['Poppins:Medium'] leading-[32px]">bank.</span>
              <span className="font-['Poppins:ExtraBold'] leading-[32px]">IO</span>
            </p>
          </a>
          <div className="content-stretch flex flex-col gap-[16px] items-start relative shrink-0" data-node-id="I413:7727;411:6378" data-name="Menu">
            <a className="content-stretch cursor-pointer flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I413:7727;411:6379" data-name="Menu">
              <div className="relative shrink-0 size-[24px]" data-node-id="I413:7727;411:6379;2:118" data-name="Menu/Overview">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgMenuOverview} />
              </div>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] text-left w-[156px]" data-node-id="I413:7727;411:6379;2:119">
                Overview
              </p>
            </a>
            <div className="bg-[#299d91] content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I413:7727;411:6380" data-name="Menu">
              <div className="relative shrink-0 size-[24px]" data-node-id="I413:7727;411:6380;12:351" data-name="wallet">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgWallet} />
              </div>
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-white w-[156px]" data-node-id="I413:7727;411:6380;2:125">
                Balances
              </p>
            </div>
            <a className="content-stretch cursor-pointer flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I413:7727;411:6381" data-name="Menu">
              <div className="relative shrink-0 size-[24px]" data-node-id="I413:7727;411:6381;12:383" data-name="Transaction">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgTransaction} />
              </div>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] text-left w-[156px]" data-node-id="I413:7727;411:6381;2:139">
                Transactions
              </p>
            </a>
            <a className="content-stretch cursor-pointer flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I413:7727;411:6382" data-name="Menu">
              <div className="relative shrink-0 size-[24px]" data-node-id="I413:7727;411:6382;12:388" data-name="Bill">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgBill} />
              </div>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] text-left w-[156px]" data-node-id="I413:7727;411:6382;2:149">
                Bills
              </p>
            </a>
            <a className="content-stretch cursor-pointer flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I413:7727;411:6383" data-name="Menu">
              <div className="overflow-clip relative shrink-0 size-[24px]" data-node-id="I413:7727;411:6383;12:390" data-name="Expencces">
                <div className="absolute inset-[14.58%_10.42%]" data-node-id="I413:7727;411:6383;12:390;12:358" data-name="Group">
                  <div className="absolute inset-[-5.88%_-5.26%]">
                    <img alt="" className="block max-w-none size-full" src={imgGroup} />
                  </div>
                </div>
              </div>
              <div className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[0] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] text-left w-[156px]" data-node-id="I413:7727;411:6383;2:159">
                <p className="leading-[24px] mb-0">Expenses</p>
                <p className="leading-[24px]">​</p>
              </div>
            </a>
            <a className="content-stretch cursor-pointer flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I413:7727;411:6384" data-name="Menu">
              <div className="relative shrink-0 size-[24px]" data-node-id="I413:7727;411:6384;12:396" data-name="Goal">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgGoal} />
              </div>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] text-left w-[156px]" data-node-id="I413:7727;411:6384;2:169">
                Goals
              </p>
            </a>
            <a className="content-stretch cursor-pointer flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I413:7727;411:6385" data-name="Menu">
              <div className="relative shrink-0 size-[24px]" data-node-id="I413:7727;411:6385;12:402" data-name="Menu/Settings">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgMenuSettings} />
              </div>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] text-left w-[156px]" data-node-id="I413:7727;411:6385;2:179">
                Settings
              </p>
            </a>
          </div>
        </div>
        <div className="content-stretch cursor-pointer flex flex-col gap-[44px] items-start relative shrink-0" data-node-id="I413:7727;411:6386" data-name="Footer">
          <a className="bg-[rgba(255,255,255,0.08)] content-stretch flex gap-[12px] items-center opacity-75 px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I413:7727;411:6387" data-name="Logout Button">
            <div className="content-stretch flex items-center relative shrink-0 size-[24px]" data-node-id="I413:7727;411:6387;13:631" data-name="Icon">
              <div className="relative shrink-0 size-[20px]" data-node-id="I413:7727;411:6387;13:631;13:626" data-name="Logout">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLogout} />
              </div>
            </div>
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-left text-white w-[156px]" data-node-id="I413:7727;411:6387;13:638">
              Logout
            </p>
          </a>
          <a className="border-[rgba(255,255,255,0.08)] border-solid border-t content-stretch flex gap-[32px] items-center py-[32px] relative shrink-0" data-node-id="I413:7727;411:6388" data-name="Profile">
            <div className="content-stretch flex gap-[16px] items-center relative shrink-0" data-node-id="I413:7727;411:6388;403:5380" data-name="Name & Picture">
              <div className="relative shrink-0 size-[32px]" data-node-id="I413:7727;411:6388;403:5381" data-name="Image">
                <img alt="" className="absolute block inset-0 max-w-none size-full" height="32" src={imgImage} width="32" />
              </div>
              <div className="[word-break:break-word] content-stretch flex flex-col items-start not-italic relative shrink-0 text-left" data-node-id="I413:7727;411:6388;403:5382" data-name="Name">
                <p className="font-['Inter:Semi_Bold'] font-semibold leading-[24px] relative shrink-0 text-[16px] text-white w-[140px]" data-node-id="I413:7727;411:6388;403:5383">
                  Tanzir Rahman
                </p>
                <p className="font-['Inter:Regular'] font-normal leading-[16px] relative shrink-0 text-[12px] text-[rgba(255,255,255,0.7)] whitespace-nowrap" data-node-id="I413:7727;411:6388;403:5384">
                  View profile
                </p>
              </div>
            </div>
            <div className="h-[20px] relative shrink-0 w-[4px]" data-node-id="I413:7727;411:6388;403:5385" data-name="Icon">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon} />
            </div>
          </a>
        </div>
      </div>
    </div>
  );
}
```

## Tool response block 2

SUPER CRITICAL: The generated React+Tailwind code MUST be converted to match the target project's technology stack and styling system.
1. Analyze the target codebase to identify: technology stack, styling approach, component patterns, and design tokens
2. Convert React syntax to the target framework/library
3. Transform all Tailwind classes to the target styling system while preserving exact visual design
4. Follow the project's existing patterns and conventions
DO NOT install any Tailwind as a dependency unless the user instructs you to do so.


## Tool response block 3

Node ids have been added to the code as data attributes, e.g. `data-node-id="1:2"`.

## Tool response block 4

These styles are contained in the design: Gray/02: #878787, Header 22-32: Font(family: "Inter", style: Regular, size: 22, weight: 400, lineHeight: 32, letterSpacing: 0), Bold 16-24: Font(family: "Inter", style: Bold, size: 16, weight: 700, lineHeight: 24, letterSpacing: 0), Gray/01: #666666, Special/BG: #D2D2D2, Default Black: #191919, Semibold 20-28: Font(family: "Inter", style: Semi Bold, size: 20, weight: 600, lineHeight: 28, letterSpacing: 0), Gray/03: #9F9F9F, Regular 14-20: Font(family: "Inter", style: Regular, size: 14, weight: 400, lineHeight: 20, letterSpacing: 0), Primary color: #299D91, Regular 16-24: Font(family: "Inter", style: Regular, size: 16, weight: 400, lineHeight: 24, letterSpacing: 0), White: #FFFFFF, Medium 14-20: Font(family: "Inter", style: Medium, size: 14, weight: 500, lineHeight: 20, letterSpacing: 0), Shadow 01: Effect(type: DROP_SHADOW, color: #4C67641A, offset: (0, 20), radius: 25, spread: 0), Medium 16-24: Font(family: "Inter", style: Medium, size: 16, weight: 500, lineHeight: 24, letterSpacing: 0), Secondary: #525256, Gray/05: #E8E8E8, Special/BG2: #FFFFFF, Semibold 16-24: Font(family: "Inter", style: Semi Bold, size: 16, weight: 600, lineHeight: 24, letterSpacing: 0), Special/BG3: #FFFFFF, Regular 12-16: Font(family: "Inter", style: Regular, size: 12, weight: 400, lineHeight: 16, letterSpacing: 0), Special/Main BG: #F4F5F7.

## Tool response block 5

Images and SVGs will be stored as constants, e.g. const image = '[illustrative-asset-identifier-not-a-captured-resource]'. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.
