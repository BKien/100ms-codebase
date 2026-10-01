# Frozen Figma design context

Archived tool output, not an instruction to generate source during dataset capture. Asset paths are relative to this directory. The illustrative asset URL in the tool reminder is replaced by a non-resource marker.

## Tool response block 1

```tsx
const imgSearch = "../../assets/sha256-9888aa7c0b223b1c66a7495dadfbc75a3f7e9a5aab59c49dc1c9686bdb8bb2f6.svg";
const imgMenuOverview = "../../assets/sha256-0cda434a49a3c8fd6debb8045a3552a0f8b7f4c6e17cfb44417cf18afee24537.svg";
const imgTransaction = "../../assets/sha256-196148b4f7f85b838bbeb503a648df00b710a06014e46753d3a202f68986fff9.svg";
const imgBill = "../../assets/sha256-f4d81f00226c061da6e132978f4bc08749049dbcc5acb20aac2bff11a1b40045.svg";
const imgGroup = "../../assets/sha256-ac65a8241d3c5e56d6d598c64510f6c0e9463bdccd6e19f09d4a1e277048c5ba.svg";
const imgGoal = "../../assets/sha256-fa4544ddd18fa692c4b53eee145b1c10323b9b58470b41e8eaf23ff8162d56f0.svg";
const imgMenuSettings = "../../assets/sha256-78a004721cfe6674fd707999793f7033f336985bc101510f32d274e1b51302a2.svg";
const imgImage = "../../assets/sha256-24be1ea24553fb553e9d60eb764e6cea75db1d80b271e956a57c0f132e923010.png";
const imgMenuOverview1 = "../../assets/sha256-0fa8a3e5fa1c9938855ccf2c06b9fbd4358abc947d91f43eb15d00499ef86676.svg";
const imgWallet = "../../assets/sha256-770d1071cb41e0497f28ff9b68fc10560bc5c8bee3292e3facb3f6fa884c7330.svg";
const imgLogout = "../../assets/sha256-c690ae811c470d066d09b8e568d175e934a4c2f04a491f1f8b78e500f29d483c.svg";
const imgIcon = "../../assets/sha256-6dc81638c4dc26974ff2d1bff954a1384d188f85298f626452a7a49ba1d39f77.svg";
const imgChevronsRight = "../../assets/sha256-c80d8dba127828568fbf27e62c7987e40d7db18638601b5d1f52674a79c46502.svg";
const imgClarityNotificationSolidBadged = "../../assets/sha256-44fdee4cf6feba7420386c9b410416034b191f18d918c52bd22ddb08810dd59c.svg";
const imgChevronRight = "../../assets/sha256-73f46492f01b4c9df9ad47a5c02d127c03304999b1d2df0198c5eefc5c9a490b.svg";
const imgChevronUp = "../../assets/sha256-3231dda63904ea60d9389407d736173597f15c99247e50116ccf62383751d216.svg";
const imgChevronRight1 = "../../assets/sha256-73f46492f01b4c9df9ad47a5c02d127c03304999b1d2df0198c5eefc5c9a490b.svg";
const imgChevronDown = "../../assets/sha256-46afb3f00c07f2ac83f1388ec73fd2507a644459ddfd9d30bf4cbea15887bec9.svg";
const imgCheck = "../../assets/sha256-29ef089800519f0ac98e74436b25e42e78ceef2b85436ee44df9e39b4e5f73b7.svg";
const imgXCircle = "../../assets/sha256-62dd2d81d5027011918e354bcdaf9eb26c66a07f7c1b51e7287ec423fda31cc2.svg";

function Search({ className }: { className?: string }) {
  return (
    <div className={className || "relative size-[24px]"} data-node-id="2798:1048" data-name="search">
      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgSearch} />
    </div>
  );
}

type MenuProps = {
  className?: string;
  status?: "Active" | "Inactive";
  type?: "Overview" | "Bills" | "Goals" | "Expenses" | "Transactions" | "Settings";
};

function Menu({ className, status = "Active", type = "Overview" }: MenuProps) {
  const isBillsAndNotStatus = type === "Bills" && status === "Inactive";
  const isExpensesAndNotStatus = type === "Expenses" && status === "Inactive";
  const isGoalsAndNotStatus = type === "Goals" && status === "Inactive";
  const isOverviewAndStatus = type === "Overview" && status === "Active";
  const isSettingsAndNotStatus = type === "Settings" && status === "Inactive";
  const isTransactionsAndNotStatus = type === "Transactions" && status === "Inactive";
  return (
    <div className={className || `content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] ${status === "Inactive" && ["Transactions", "Bills", "Expenses", "Goals", "Settings"].includes(type) ? "" : "bg-[#299d91]"}`} id={isSettingsAndNotStatus ? "node-2798_998" : isGoalsAndNotStatus ? "node-2798_989" : isExpensesAndNotStatus ? "node-2798_980" : isBillsAndNotStatus ? "node-2798_971" : isTransactionsAndNotStatus ? "node-2798_962" : "node-2798_941"}>
      {isOverviewAndStatus && (
        <>
          <div className="relative shrink-0 size-[24px]" data-node-id="2798:942" data-name="Menu/Overview">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgMenuOverview} />
          </div>
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-white w-[156px]" data-node-id="2798:943">
            Overview
          </p>
        </>
      )}
      {isTransactionsAndNotStatus && (
        <>
          <div className="relative shrink-0 size-[24px]" data-node-id="2798:963" data-name="Transaction">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgTransaction} />
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] w-[156px]" data-node-id="2798:964">
            Transactions
          </p>
        </>
      )}
      {isBillsAndNotStatus && (
        <>
          <div className="relative shrink-0 size-[24px]" data-node-id="2798:972" data-name="Bill">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgBill} />
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] w-[156px]" data-node-id="2798:973">
            Bills
          </p>
        </>
      )}
      {isExpensesAndNotStatus && (
        <>
          <div className="overflow-clip relative shrink-0 size-[24px]" data-node-id="2798:981" data-name="Expencces">
            <div className="absolute inset-[14.58%_10.42%]" data-node-id="I2798:981;12:358" data-name="Group">
              <div className="absolute inset-[-5.88%_-5.26%]">
                <img alt="" className="block max-w-none size-full" src={imgGroup} />
              </div>
            </div>
          </div>
          <div className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[0] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] w-[156px]" data-node-id="2798:982">
            <p className="leading-[24px] mb-0">Expenses</p>
            <p className="leading-[24px]">​</p>
          </div>
        </>
      )}
      {isGoalsAndNotStatus && (
        <>
          <div className="relative shrink-0 size-[24px]" data-node-id="2798:990" data-name="Goal">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgGoal} />
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] w-[156px]" data-node-id="2798:991">
            Goals
          </p>
        </>
      )}
      {isSettingsAndNotStatus && (
        <>
          <div className="relative shrink-0 size-[24px]" data-node-id="2798:999" data-name="Menu/Settings">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgMenuSettings} />
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] w-[156px]" data-node-id="2798:1000">
            Settings
          </p>
        </>
      )}
    </div>
  );
}

export default function Component106110621063() {
  return (
    <div className="relative size-full" data-node-id="2929:1679" data-name="106.1, 106.2, 106.3">
      <div className="absolute h-[1024px] left-0 top-0 w-[1440px]" data-node-id="2925:1686" data-name="106.1 Edit Details">
        <div className="absolute bg-[#191919] content-stretch flex flex-col gap-[228px] items-start left-0 px-[28px] py-[48px] top-0" data-node-id="2798:2213" data-name="Nav bar">
          <div className="content-stretch flex flex-col gap-[40px] items-start relative shrink-0" data-node-id="I2798:2213;411:6376" data-name="Logo & Menu">
            <p className="[word-break:break-word] font-['Poppins:Bold'] leading-[0] not-italic relative shrink-0 text-[0px] text-center text-white tracking-[1.92px] w-[224px]" data-node-id="I2798:2213;411:6377">
              <span className="font-['Poppins:ExtraBold'] leading-[32px] text-[24px]">FINE</span>
              <span className="font-['Poppins:Medium'] leading-[32px] text-[24px]">bank.</span>
              <span className="font-['Poppins:ExtraBold'] leading-[32px] text-[24px]">IO</span>
            </p>
            <div className="content-stretch flex flex-col gap-[16px] items-start relative shrink-0" data-node-id="I2798:2213;411:6378" data-name="Menu">
              <div className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2213;411:6379" data-name="Menu">
                <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2213;411:6379;2:118" data-name="Menu/Overview">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgMenuOverview1} />
                </div>
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] w-[156px]" data-node-id="I2798:2213;411:6379;2:119">
                  Overview
                </p>
              </div>
              <div className="bg-[#299d91] content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2213;411:6380" data-name="Menu">
                <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2213;411:6380;12:351" data-name="wallet">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgWallet} />
                </div>
                <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-white w-[156px]" data-node-id="I2798:2213;411:6380;2:125">
                  Balances
                </p>
              </div>
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Transactions" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Bills" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Expenses" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Goals" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Settings" />
            </div>
          </div>
          <div className="content-stretch flex flex-col gap-[44px] items-start relative shrink-0" data-node-id="I2798:2213;411:6386" data-name="Footer">
            <div className="bg-[rgba(255,255,255,0.08)] content-stretch flex gap-[12px] items-center opacity-75 px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2213;411:6387" data-name="Logout Button">
              <div className="content-stretch flex items-center relative shrink-0 size-[24px]" data-node-id="I2798:2213;411:6387;13:631" data-name="Icon">
                <div className="relative shrink-0 size-[20px]" data-node-id="I2798:2213;411:6387;13:631;13:626" data-name="Logout">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLogout} />
                </div>
              </div>
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-white w-[156px]" data-node-id="I2798:2213;411:6387;13:638">
                Logout
              </p>
            </div>
            <div className="border-[rgba(255,255,255,0.08)] border-solid border-t content-stretch flex gap-[32px] items-center py-[32px] relative shrink-0" data-node-id="I2798:2213;411:6388" data-name="Profile">
              <div className="content-stretch flex gap-[16px] items-center relative shrink-0" data-node-id="I2798:2213;411:6388;403:5380" data-name="Name & Picture">
                <div className="relative shrink-0 size-[32px]" data-node-id="I2798:2213;411:6388;403:5381" data-name="Image">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" height="32" src={imgImage} width="32" />
                </div>
                <div className="[word-break:break-word] content-stretch flex flex-col items-start not-italic relative shrink-0" data-node-id="I2798:2213;411:6388;403:5382" data-name="Name">
                  <p className="font-['Inter:Semi_Bold'] font-semibold leading-[24px] relative shrink-0 text-[16px] text-white w-[140px]" data-node-id="I2798:2213;411:6388;403:5383">
                    Tanzir Rahman
                  </p>
                  <p className="font-['Inter:Regular'] font-normal leading-[16px] relative shrink-0 text-[12px] text-[rgba(255,255,255,0.7)] whitespace-nowrap" data-node-id="I2798:2213;411:6388;403:5384">
                    View profile
                  </p>
                </div>
              </div>
              <div className="h-[20px] relative shrink-0 w-[4px]" data-node-id="I2798:2213;411:6388;403:5385" data-name="Icon">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon} />
              </div>
            </div>
          </div>
        </div>
        <div className="absolute content-stretch flex flex-col h-[1024px] items-start left-[280px] top-0 w-[1160px]" data-node-id="2798:2214" data-name="Frame">
          <div className="border-[#e8e8e8] border-b border-solid content-stretch flex items-center justify-between pl-[24px] pr-[32px] py-[20px] relative shrink-0 w-full" data-node-id="2798:2215" data-name="Header">
            <div className="content-stretch flex gap-[24px] items-center relative shrink-0" data-node-id="I2798:2215;411:6047" data-name="Header">
              <p className="[word-break:break-word] font-['Inter:Bold'] font-bold leading-[28px] not-italic relative shrink-0 text-[#191919] text-[24px] w-[140px]" data-node-id="I2798:2215;411:6048">
                Edit
                <br aria-hidden />
                Details
              </p>
              <div className="content-stretch flex gap-[4px] items-center relative shrink-0" data-node-id="I2798:2215;411:6049" data-name="Date">
                <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2215;411:6050" data-name="chevrons-right">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronsRight} />
                </div>
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[#9f9f9f] text-[14px] whitespace-nowrap" data-node-id="I2798:2215;411:6053">
                  May 19, 2023
                </p>
              </div>
            </div>
            <div className="content-stretch flex gap-[40px] items-center relative shrink-0" data-node-id="I2798:2215;411:6054" data-name="Search">
              <div className="content-stretch flex items-center relative shrink-0" data-node-id="I2798:2215;411:6055" data-name="Notification icon">
                <div className="grid-cols-[max-content] grid-rows-[max-content] inline-grid leading-[0] place-items-start relative shrink-0" data-node-id="I2798:2215;411:6055;2:622">
                  <div className="col-1 ml-0 mt-0 relative row-1 size-[24px]" data-node-id="I2798:2215;411:6055;2:623" data-name="clarity:notification-solid-badged">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgClarityNotificationSolidBadged} />
                  </div>
                </div>
              </div>
              <div className="bg-white content-stretch drop-shadow-[0px_26px_13px_rgba(106,22,58,0.04)] flex gap-[170px] items-start pl-[32px] pr-[24px] py-[12px] relative rounded-[12px] shrink-0" data-node-id="I2798:2215;411:6056" data-name="Search">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#9f9f9f] text-[16px] w-[102px]" data-node-id="I2798:2215;411:6056;404:5259">
                  Search here
                </p>
                <Search className="relative shrink-0 size-[24px]" />
              </div>
            </div>
          </div>
          <div className="bg-[#f4f5f7] content-stretch flex flex-col gap-[24px] items-start px-[40px] py-[32px] relative shrink-0 w-full" data-node-id="2798:2216" data-name="Content Inner">
            <div className="content-stretch flex gap-[8px] items-center relative shrink-0" data-node-id="2798:2217" data-name="Breadcrumb">
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[#666] text-[14px] whitespace-nowrap" data-node-id="2798:2218">
                Balances
              </p>
              <div className="relative shrink-0 size-[12px]" data-node-id="2798:2219" data-name="chevron-right">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronRight} />
              </div>
              <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#299d91] text-[14px] whitespace-nowrap" data-node-id="2798:2221">
                Edit details
              </p>
            </div>
            <div className="content-stretch flex items-start justify-center relative shrink-0 w-full" data-node-id="2798:2222" data-name="Form Align Container">
              <div className="bg-white content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col gap-[24px] items-start p-[40px] relative rounded-[12px] shrink-0 w-[560px]" data-node-id="2798:2223" data-name="Add Account Form">
                <p className="[word-break:break-word] capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] not-italic relative shrink-0 text-[#191919] text-[20px] w-full" data-node-id="2798:2224">
                  Edit details
                </p>
                <div className="content-stretch flex flex-col gap-[20px] items-start relative shrink-0 w-full" data-node-id="2798:2225" data-name="Fields Stack">
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2226" data-name="Field - Account Type">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2227">
                      Account Type
                    </p>
                    <div className="border border-[#299d91] border-solid content-stretch flex h-[48px] items-center justify-between px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2228" data-name="Select Input Box">
                      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#191919] text-[16px] whitespace-nowrap" data-node-id="2798:2229">
                        Checking
                      </p>
                      <div className="relative shrink-0 size-[16px]" data-node-id="2798:2230" data-name="chevron-up">
                        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronUp} />
                      </div>
                    </div>
                    <div className="bg-white border border-[#e4e7eb] border-solid content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col gap-[4px] items-start p-[8px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2232" data-name="Dropdown Menu Container">
                      <div className="content-stretch flex items-start px-[12px] py-[10px] relative rounded-[6px] shrink-0 w-full" data-node-id="2798:2233" data-name="Option - Credit Card">
                        <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[20px] min-w-px not-italic relative text-[#191d23] text-[14px]" data-node-id="2798:2234">
                          Credit Card
                        </p>
                      </div>
                      <div className="bg-[#299d91] content-stretch flex items-start px-[12px] py-[10px] relative rounded-[6px] shrink-0 w-full" data-node-id="2798:2235" data-name="Option - Checking (Hovered)">
                        <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Semi_Bold'] font-semibold leading-[24px] min-w-px not-italic relative text-[16px] text-white" data-node-id="2798:2236">
                          Checking
                        </p>
                      </div>
                      <div className="content-stretch flex items-start px-[12px] py-[10px] relative rounded-[6px] shrink-0 w-full" data-node-id="2798:2237" data-name="Option - Savings">
                        <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[20px] min-w-px not-italic relative text-[#191d23] text-[14px]" data-node-id="2798:2238">
                          Savings
                        </p>
                      </div>
                      <div className="content-stretch flex items-start px-[12px] py-[10px] relative rounded-[6px] shrink-0 w-full" data-node-id="2798:2239" data-name="Option - Investment">
                        <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[20px] min-w-px not-italic relative text-[#191d23] text-[14px]" data-node-id="2798:2240">
                          Investment
                        </p>
                      </div>
                      <div className="content-stretch flex items-start px-[12px] py-[10px] relative rounded-[6px] shrink-0 w-full" data-node-id="2798:2241" data-name="Option - Loan">
                        <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[20px] min-w-px not-italic relative text-[#191d23] text-[14px]" data-node-id="2798:2242">
                          Loan
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2243" data-name="Field - Bank Name">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2244">
                      Bank Name
                    </p>
                    <div className="border border-[#d0d5dd] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2245" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[16px] text-black" data-node-id="2798:2246">
                        AB Bank LTd.
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2247" data-name="Field - Branch Name">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2248">
                      Branch Name (Optional)
                    </p>
                    <div className="border border-[#d0d5dd] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2249" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[16px] text-black" data-node-id="2798:2250">
                        Park Street Branch
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2251" data-name="Field - Account Number">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2252">
                      Account Number
                    </p>
                    <div className="border border-[#d0d5dd] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2253" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[16px] text-black" data-node-id="2798:2254">
                        1234 1234
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2255" data-name="Field - Initial Balance">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2256">
                      Initial Balance
                    </p>
                    <div className="border border-[#d0d5dd] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2257" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[16px] text-black" data-node-id="2798:2258">
                        $30,25.00
                      </p>
                    </div>
                  </div>
                </div>
                <div className="content-stretch flex gap-[24px] items-center relative shrink-0 w-full" data-node-id="2798:2259" data-name="Action Buttons">
                  <div className="bg-[#299d91] content-stretch flex flex-[1_0_0] h-[48px] items-center justify-center min-w-px px-[32px] py-[12px] relative rounded-[4px]" data-node-id="2798:2260" data-name="Submit Button">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-white whitespace-nowrap" data-node-id="2798:2261">
                      Save changes
                    </p>
                  </div>
                  <div className="content-stretch flex items-center p-[8px] relative shrink-0" data-node-id="2798:2262" data-name="Cancel Button">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[#666] text-[16px] whitespace-nowrap" data-node-id="2798:2263">
                      Cancel
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="absolute h-[1024px] left-0 top-[1205px] w-[1440px]" data-node-id="2925:1685" data-name="106.2 Input Validation for Editing Account Details">
        <div className="absolute bg-[#191919] content-stretch flex flex-col gap-[228px] items-start left-0 px-[28px] py-[48px] top-0" data-node-id="2798:2311" data-name="Nav bar">
          <div className="content-stretch flex flex-col gap-[40px] items-start relative shrink-0" data-node-id="I2798:2311;411:6376" data-name="Logo & Menu">
            <p className="[word-break:break-word] font-['Poppins:Bold'] leading-[0] not-italic relative shrink-0 text-[0px] text-center text-white tracking-[1.92px] w-[224px]" data-node-id="I2798:2311;411:6377">
              <span className="font-['Poppins:ExtraBold'] leading-[32px] text-[24px]">FINE</span>
              <span className="font-['Poppins:Medium'] leading-[32px] text-[24px]">bank.</span>
              <span className="font-['Poppins:ExtraBold'] leading-[32px] text-[24px]">IO</span>
            </p>
            <div className="content-stretch flex flex-col gap-[16px] items-start relative shrink-0" data-node-id="I2798:2311;411:6378" data-name="Menu">
              <div className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2311;411:6379" data-name="Menu">
                <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2311;411:6379;2:118" data-name="Menu/Overview">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgMenuOverview1} />
                </div>
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] w-[156px]" data-node-id="I2798:2311;411:6379;2:119">
                  Overview
                </p>
              </div>
              <div className="bg-[#299d91] content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2311;411:6380" data-name="Menu">
                <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2311;411:6380;12:351" data-name="wallet">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgWallet} />
                </div>
                <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-white w-[156px]" data-node-id="I2798:2311;411:6380;2:125">
                  Balances
                </p>
              </div>
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Transactions" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Bills" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Expenses" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Goals" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Settings" />
            </div>
          </div>
          <div className="content-stretch flex flex-col gap-[44px] items-start relative shrink-0" data-node-id="I2798:2311;411:6386" data-name="Footer">
            <div className="bg-[rgba(255,255,255,0.08)] content-stretch flex gap-[12px] items-center opacity-75 px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2311;411:6387" data-name="Logout Button">
              <div className="content-stretch flex items-center relative shrink-0 size-[24px]" data-node-id="I2798:2311;411:6387;13:631" data-name="Icon">
                <div className="relative shrink-0 size-[20px]" data-node-id="I2798:2311;411:6387;13:631;13:626" data-name="Logout">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLogout} />
                </div>
              </div>
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-white w-[156px]" data-node-id="I2798:2311;411:6387;13:638">
                Logout
              </p>
            </div>
            <div className="border-[rgba(255,255,255,0.08)] border-solid border-t content-stretch flex gap-[32px] items-center py-[32px] relative shrink-0" data-node-id="I2798:2311;411:6388" data-name="Profile">
              <div className="content-stretch flex gap-[16px] items-center relative shrink-0" data-node-id="I2798:2311;411:6388;403:5380" data-name="Name & Picture">
                <div className="relative shrink-0 size-[32px]" data-node-id="I2798:2311;411:6388;403:5381" data-name="Image">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" height="32" src={imgImage} width="32" />
                </div>
                <div className="[word-break:break-word] content-stretch flex flex-col items-start not-italic relative shrink-0" data-node-id="I2798:2311;411:6388;403:5382" data-name="Name">
                  <p className="font-['Inter:Semi_Bold'] font-semibold leading-[24px] relative shrink-0 text-[16px] text-white w-[140px]" data-node-id="I2798:2311;411:6388;403:5383">
                    Tanzir Rahman
                  </p>
                  <p className="font-['Inter:Regular'] font-normal leading-[16px] relative shrink-0 text-[12px] text-[rgba(255,255,255,0.7)] whitespace-nowrap" data-node-id="I2798:2311;411:6388;403:5384">
                    View profile
                  </p>
                </div>
              </div>
              <div className="h-[20px] relative shrink-0 w-[4px]" data-node-id="I2798:2311;411:6388;403:5385" data-name="Icon">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon} />
              </div>
            </div>
          </div>
        </div>
        <div className="absolute content-stretch flex flex-col h-[1024px] items-start left-[280px] top-0 w-[1160px]" data-node-id="2798:2312" data-name="Main Content Pane">
          <div className="border-[#e8e8e8] border-b border-solid content-stretch flex items-center justify-between pl-[24px] pr-[32px] py-[20px] relative shrink-0 w-full" data-node-id="2798:2313" data-name="Header">
            <div className="content-stretch flex gap-[24px] items-center relative shrink-0" data-node-id="I2798:2313;411:6047" data-name="Header">
              <p className="[word-break:break-word] font-['Inter:Bold'] font-bold leading-[28px] not-italic relative shrink-0 text-[#191919] text-[24px] w-[140px]" data-node-id="I2798:2313;411:6048">
                Edit
                <br aria-hidden />
                Details
              </p>
              <div className="content-stretch flex gap-[4px] items-center relative shrink-0" data-node-id="I2798:2313;411:6049" data-name="Date">
                <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2313;411:6050" data-name="chevrons-right">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronsRight} />
                </div>
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[#9f9f9f] text-[14px] whitespace-nowrap" data-node-id="I2798:2313;411:6053">
                  May 19, 2023
                </p>
              </div>
            </div>
            <div className="content-stretch flex gap-[40px] items-center relative shrink-0" data-node-id="I2798:2313;411:6054" data-name="Search">
              <div className="content-stretch flex items-center relative shrink-0" data-node-id="I2798:2313;411:6055" data-name="Notification icon">
                <div className="grid-cols-[max-content] grid-rows-[max-content] inline-grid leading-[0] place-items-start relative shrink-0" data-node-id="I2798:2313;411:6055;2:622">
                  <div className="col-1 ml-0 mt-0 relative row-1 size-[24px]" data-node-id="I2798:2313;411:6055;2:623" data-name="clarity:notification-solid-badged">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgClarityNotificationSolidBadged} />
                  </div>
                </div>
              </div>
              <div className="bg-white content-stretch drop-shadow-[0px_26px_13px_rgba(106,22,58,0.04)] flex gap-[170px] items-start pl-[32px] pr-[24px] py-[12px] relative rounded-[12px] shrink-0" data-node-id="I2798:2313;411:6056" data-name="Search">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#9f9f9f] text-[16px] w-[102px]" data-node-id="I2798:2313;411:6056;404:5259">
                  Search here
                </p>
                <Search className="relative shrink-0 size-[24px]" />
              </div>
            </div>
          </div>
          <div className="bg-[#f4f5f7] content-stretch flex flex-[1_0_0] flex-col gap-[24px] items-start min-h-px px-[40px] py-[32px] relative w-full" data-node-id="2798:2314" data-name="Content Inner">
            <div className="content-stretch flex gap-[8px] items-center relative shrink-0" data-node-id="2798:2315" data-name="Breadcrumb">
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[#666] text-[14px] whitespace-nowrap" data-node-id="2798:2316">
                Balances
              </p>
              <div className="relative shrink-0 size-[12px]" data-node-id="2798:2317" data-name="chevron-right">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronRight1} />
              </div>
              <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#299d91] text-[14px] whitespace-nowrap" data-node-id="2798:2319">
                Edit details
              </p>
            </div>
            <div className="content-stretch flex items-start justify-center relative shrink-0 w-full" data-node-id="2798:2320" data-name="Form Align Container">
              <div className="bg-white content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col gap-[24px] items-start p-[40px] relative rounded-[12px] shrink-0 w-[560px]" data-node-id="2798:2321" data-name="Add Account Form">
                <p className="[word-break:break-word] capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] not-italic relative shrink-0 text-[#191919] text-[20px] w-full" data-node-id="2798:2322">
                  Edit details
                </p>
                <div className="content-stretch flex flex-col gap-[20px] items-start relative shrink-0 w-full" data-node-id="2798:2323" data-name="Fields Stack">
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2324" data-name="Field - Account Type">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] min-w-full not-italic relative shrink-0 text-[#191d23] text-[14px] w-[min-content]" data-node-id="2798:2325">
                      Account Type
                    </p>
                    <div className="border border-[#d92d20] border-solid content-stretch flex h-[48px] items-center justify-between px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2326" data-name="Select Input Box">
                      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#999da3] text-[16px] whitespace-nowrap" data-node-id="2798:2327">
                        Select account type
                      </p>
                      <div className="overflow-clip relative shrink-0 size-[16px]" data-node-id="2798:2328" data-name="chevron-down">
                        <div className="absolute bottom-[37.5%] left-1/4 right-1/4 top-[37.5%]" data-node-id="2798:2329" data-name="chevron-down">
                          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronDown} />
                        </div>
                      </div>
                    </div>
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[16px] not-italic relative shrink-0 text-[#d92d20] text-[12px] whitespace-nowrap" data-node-id="2798:2331">
                      This field is required
                    </p>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2332" data-name="Field - Bank Name">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] min-w-full not-italic relative shrink-0 text-[#191d23] text-[14px] w-[min-content]" data-node-id="2798:2333">
                      Bank Name
                    </p>
                    <div className="border border-[#d92d20] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2334" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[#999da3] text-[16px]" data-node-id="2798:2335">
                        Enter bank name
                      </p>
                    </div>
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[16px] not-italic relative shrink-0 text-[#d92d20] text-[12px] whitespace-nowrap" data-node-id="2798:2336">
                      This field is required
                    </p>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2337" data-name="Field - Branch Name">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2338">
                      Branch Name (Optional)
                    </p>
                    <div className="border border-[#d0d5dd] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2339" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[#999da3] text-[16px]" data-node-id="2798:2340">
                        Enter branch name
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2341" data-name="Field - Account Number">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] min-w-full not-italic relative shrink-0 text-[#191d23] text-[14px] w-[min-content]" data-node-id="2798:2342">
                      Account Number
                    </p>
                    <div className="border border-[#d92d20] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2343" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[#999da3] text-[16px]" data-node-id="2798:2344">
                        Enter account number
                      </p>
                    </div>
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[16px] not-italic relative shrink-0 text-[#d92d20] text-[12px] whitespace-nowrap" data-node-id="2798:2345">
                      This field is required
                    </p>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2346" data-name="Field - Initial Balance">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] min-w-full not-italic relative shrink-0 text-[#191d23] text-[14px] w-[min-content]" data-node-id="2798:2347">
                      Initial Balance
                    </p>
                    <div className="border border-[#d92d20] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2348" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[#999da3] text-[16px]" data-node-id="2798:2349">
                        $0.00
                      </p>
                    </div>
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[16px] not-italic relative shrink-0 text-[#d92d20] text-[12px] whitespace-nowrap" data-node-id="2798:2350">
                      This field is required
                    </p>
                  </div>
                </div>
                <div className="content-stretch flex gap-[24px] items-center relative shrink-0 w-full" data-node-id="2798:2351" data-name="Action Buttons">
                  <div className="bg-[#299d91] content-stretch flex flex-[1_0_0] h-[48px] items-center justify-center min-w-px px-[32px] py-[12px] relative rounded-[4px]" data-node-id="2798:2352" data-name="Submit Button">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-white whitespace-nowrap" data-node-id="2798:2353">
                      Save changes
                    </p>
                  </div>
                  <div className="content-stretch flex items-center p-[8px] relative shrink-0" data-node-id="2798:2354" data-name="Cancel Button">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[#666] text-[16px] whitespace-nowrap" data-node-id="2798:2355">
                      Cancel
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="absolute h-[1024px] left-0 top-[2423px] w-[1440px]" data-node-id="2925:1684" data-name="106.3 Edit Details - Success Toast Notification">
        <div className="absolute bg-[#191919] content-stretch flex flex-col gap-[228px] items-start left-0 px-[28px] py-[48px] top-0" data-node-id="2798:2419" data-name="Nav bar">
          <div className="content-stretch flex flex-col gap-[40px] items-start relative shrink-0" data-node-id="I2798:2419;411:6376" data-name="Logo & Menu">
            <p className="[word-break:break-word] font-['Poppins:Bold'] leading-[0] not-italic relative shrink-0 text-[0px] text-center text-white tracking-[1.92px] w-[224px]" data-node-id="I2798:2419;411:6377">
              <span className="font-['Poppins:ExtraBold'] leading-[32px] text-[24px]">FINE</span>
              <span className="font-['Poppins:Medium'] leading-[32px] text-[24px]">bank.</span>
              <span className="font-['Poppins:ExtraBold'] leading-[32px] text-[24px]">IO</span>
            </p>
            <div className="content-stretch flex flex-col gap-[16px] items-start relative shrink-0" data-node-id="I2798:2419;411:6378" data-name="Menu">
              <div className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2419;411:6379" data-name="Menu">
                <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2419;411:6379;2:118" data-name="Menu/Overview">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgMenuOverview1} />
                </div>
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] w-[156px]" data-node-id="I2798:2419;411:6379;2:119">
                  Overview
                </p>
              </div>
              <div className="bg-[#299d91] content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2419;411:6380" data-name="Menu">
                <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2419;411:6380;12:351" data-name="wallet">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgWallet} />
                </div>
                <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-white w-[156px]" data-node-id="I2798:2419;411:6380;2:125">
                  Balances
                </p>
              </div>
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Transactions" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Bills" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Expenses" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Goals" />
              <Menu className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" status="Inactive" type="Settings" />
            </div>
          </div>
          <div className="content-stretch flex flex-col gap-[44px] items-start relative shrink-0" data-node-id="I2798:2419;411:6386" data-name="Footer">
            <div className="bg-[rgba(255,255,255,0.08)] content-stretch flex gap-[12px] items-center opacity-75 px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2419;411:6387" data-name="Logout Button">
              <div className="content-stretch flex items-center relative shrink-0 size-[24px]" data-node-id="I2798:2419;411:6387;13:631" data-name="Icon">
                <div className="relative shrink-0 size-[20px]" data-node-id="I2798:2419;411:6387;13:631;13:626" data-name="Logout">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLogout} />
                </div>
              </div>
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-white w-[156px]" data-node-id="I2798:2419;411:6387;13:638">
                Logout
              </p>
            </div>
            <div className="border-[rgba(255,255,255,0.08)] border-solid border-t content-stretch flex gap-[32px] items-center py-[32px] relative shrink-0" data-node-id="I2798:2419;411:6388" data-name="Profile">
              <div className="content-stretch flex gap-[16px] items-center relative shrink-0" data-node-id="I2798:2419;411:6388;403:5380" data-name="Name & Picture">
                <div className="relative shrink-0 size-[32px]" data-node-id="I2798:2419;411:6388;403:5381" data-name="Image">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" height="32" src={imgImage} width="32" />
                </div>
                <div className="[word-break:break-word] content-stretch flex flex-col items-start not-italic relative shrink-0" data-node-id="I2798:2419;411:6388;403:5382" data-name="Name">
                  <p className="font-['Inter:Semi_Bold'] font-semibold leading-[24px] relative shrink-0 text-[16px] text-white w-[140px]" data-node-id="I2798:2419;411:6388;403:5383">
                    Tanzir Rahman
                  </p>
                  <p className="font-['Inter:Regular'] font-normal leading-[16px] relative shrink-0 text-[12px] text-[rgba(255,255,255,0.7)] whitespace-nowrap" data-node-id="I2798:2419;411:6388;403:5384">
                    View profile
                  </p>
                </div>
              </div>
              <div className="h-[20px] relative shrink-0 w-[4px]" data-node-id="I2798:2419;411:6388;403:5385" data-name="Icon">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon} />
              </div>
            </div>
          </div>
        </div>
        <div className="absolute content-stretch flex flex-col h-[1024px] items-start left-[280px] top-0 w-[1160px]" data-node-id="2798:2420" data-name="Frame">
          <div className="border-[#e8e8e8] border-b border-solid content-stretch flex items-center justify-between pl-[24px] pr-[32px] py-[20px] relative shrink-0 w-full" data-node-id="2798:2421" data-name="Header">
            <div className="content-stretch flex gap-[24px] items-center relative shrink-0" data-node-id="I2798:2421;411:6047" data-name="Header">
              <p className="[word-break:break-word] font-['Inter:Bold'] font-bold leading-[28px] not-italic relative shrink-0 text-[#191919] text-[24px] w-[140px]" data-node-id="I2798:2421;411:6048">
                Edit
                <br aria-hidden />
                Details
              </p>
              <div className="content-stretch flex gap-[4px] items-center relative shrink-0" data-node-id="I2798:2421;411:6049" data-name="Date">
                <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2421;411:6050" data-name="chevrons-right">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronsRight} />
                </div>
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[#9f9f9f] text-[14px] whitespace-nowrap" data-node-id="I2798:2421;411:6053">
                  May 19, 2023
                </p>
              </div>
            </div>
            <div className="content-stretch flex gap-[40px] items-center relative shrink-0" data-node-id="I2798:2421;411:6054" data-name="Search">
              <div className="content-stretch flex items-center relative shrink-0" data-node-id="I2798:2421;411:6055" data-name="Notification icon">
                <div className="grid-cols-[max-content] grid-rows-[max-content] inline-grid leading-[0] place-items-start relative shrink-0" data-node-id="I2798:2421;411:6055;2:622">
                  <div className="col-1 ml-0 mt-0 relative row-1 size-[24px]" data-node-id="I2798:2421;411:6055;2:623" data-name="clarity:notification-solid-badged">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgClarityNotificationSolidBadged} />
                  </div>
                </div>
              </div>
              <div className="bg-white content-stretch drop-shadow-[0px_26px_13px_rgba(106,22,58,0.04)] flex gap-[170px] items-start pl-[32px] pr-[24px] py-[12px] relative rounded-[12px] shrink-0" data-node-id="I2798:2421;411:6056" data-name="Search">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#9f9f9f] text-[16px] w-[102px]" data-node-id="I2798:2421;411:6056;404:5259">
                  Search here
                </p>
                <Search className="relative shrink-0 size-[24px]" />
              </div>
            </div>
          </div>
          <div className="bg-[#f4f5f7] content-stretch flex flex-col gap-[24px] items-start px-[40px] py-[32px] relative shrink-0 w-full" data-node-id="2798:2422" data-name="Content Inner">
            <div className="content-stretch flex gap-[8px] items-center relative shrink-0" data-node-id="2798:2423" data-name="Breadcrumb">
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[#666] text-[14px] whitespace-nowrap" data-node-id="2798:2424">
                Balances
              </p>
              <div className="relative shrink-0 size-[12px]" data-node-id="2798:2425" data-name="chevron-right">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronRight} />
              </div>
              <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#299d91] text-[14px] whitespace-nowrap" data-node-id="2798:2427">
                Edit details
              </p>
            </div>
            <div className="content-stretch flex items-start justify-center relative shrink-0 w-full" data-node-id="2798:2428" data-name="Form Align Container">
              <div className="bg-white content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col gap-[24px] items-start p-[40px] relative rounded-[12px] shrink-0 w-[560px]" data-node-id="2798:2429" data-name="Add Account Form">
                <p className="[word-break:break-word] capitalize font-['Inter:Semi_Bold'] font-semibold leading-[28px] not-italic relative shrink-0 text-[#191919] text-[20px] w-full" data-node-id="2798:2430">
                  Edit details
                </p>
                <div className="content-stretch flex flex-col gap-[20px] items-start relative shrink-0 w-full" data-node-id="2798:2431" data-name="Fields Stack">
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2432" data-name="Field - Account Type">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2433">
                      Account Type
                    </p>
                    <div className="border border-[#299d91] border-solid content-stretch flex h-[48px] items-center justify-between px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2434" data-name="Select Input Box">
                      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#191919] text-[16px] whitespace-nowrap" data-node-id="2798:2435">
                        Checking
                      </p>
                      <div className="relative shrink-0 size-[16px]" data-node-id="2798:2436" data-name="chevron-up">
                        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronUp} />
                      </div>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2438" data-name="Field - Bank Name">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2439">
                      Bank Name
                    </p>
                    <div className="border border-[#d0d5dd] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2440" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[16px] text-black" data-node-id="2798:2441">
                        AB Bank LTd.
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2442" data-name="Field - Branch Name">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2443">
                      Branch Name (Optional)
                    </p>
                    <div className="border border-[#d0d5dd] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2444" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[16px] text-black" data-node-id="2798:2445">
                        Park Street Branch
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2446" data-name="Field - Account Number">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2447">
                      Account Number
                    </p>
                    <div className="border border-[#d0d5dd] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2448" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[16px] text-black" data-node-id="2798:2449">
                        1234 1234
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="2798:2450" data-name="Field - Initial Balance">
                    <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] w-full" data-node-id="2798:2451">
                      Initial Balance
                    </p>
                    <div className="border border-[#d0d5dd] border-solid content-stretch flex h-[48px] items-center px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-full" data-node-id="2798:2452" data-name="Input Frame">
                      <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[24px] min-w-px not-italic relative text-[16px] text-black" data-node-id="2798:2453">
                        $30,25.00
                      </p>
                    </div>
                  </div>
                </div>
                <div className="content-stretch flex gap-[24px] items-center relative shrink-0 w-full" data-node-id="2798:2454" data-name="Action Buttons">
                  <div className="bg-[#299d91] content-stretch flex flex-[1_0_0] h-[48px] items-center justify-center min-w-px px-[32px] py-[12px] relative rounded-[4px]" data-node-id="2798:2455" data-name="Submit Button">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-white whitespace-nowrap" data-node-id="2798:2456">
                      Save changes
                    </p>
                  </div>
                  <div className="content-stretch flex items-center p-[8px] relative shrink-0" data-node-id="2798:2457" data-name="Cancel Button">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[#666] text-[16px] whitespace-nowrap" data-node-id="2798:2458">
                      Cancel
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div className="absolute bg-white border-[#299d91] border-l-4 border-solid content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex gap-[12px] items-center px-[16px] py-[14px] right-[40px] rounded-[8px] top-[82px]" data-node-id="2798:2459" data-name="Success Toast">
              <div className="aspect-[20/100] bg-[#299d91] content-stretch flex items-center justify-center p-[4px] relative rounded-[99px] shrink-0" data-node-id="2798:2460" data-name="Success Badge">
                <div className="relative shrink-0 size-[10px]" data-node-id="2798:2461" data-name="check">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgCheck} />
                </div>
              </div>
              <p className="[word-break:break-word] capitalize font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[#191d23] text-[14px] whitespace-nowrap" data-node-id="2798:2463">
                Account updated successfully!
              </p>
              <div className="content-stretch flex items-center justify-center p-[4px] relative shrink-0" data-node-id="2798:2464" data-name="Close Icon wrapper">
                <div className="relative shrink-0 size-[10px]" data-node-id="2798:2465" data-name="x-circle">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgXCircle} />
                </div>
              </div>
            </div>
          </div>
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

These styles are contained in the design: White: #FFFFFF, Special/BG2: #FFFFFF, Regular 16-24: Font(family: "Inter", style: Regular, size: 16, weight: 400, lineHeight: 24, letterSpacing: 0), Semibold 16-24: Font(family: "Inter", style: Semi Bold, size: 16, weight: 600, lineHeight: 24, letterSpacing: 0), Primary color: #299D91, Special/BG3: #FFFFFF, Regular 12-16: Font(family: "Inter", style: Regular, size: 12, weight: 400, lineHeight: 16, letterSpacing: 0), Default Black: #191919, Bold 24-28: Font(family: "Inter", style: Bold, size: 24, weight: 700, lineHeight: 28, letterSpacing: 0), Gray/03: #D0D5DD, Regular 14-20: Font(family: "Inter", style: Regular, size: 14, weight: 400, lineHeight: 20, letterSpacing: 0), Gray/01: #666666, Secondary: #525256, Gray/05: #E8E8E8, Medium 14-20: Font(family: "Inter", style: Medium, size: 14, weight: 500, lineHeight: 20, letterSpacing: 0), Semibold 20-28: Font(family: "Inter", style: Semi Bold, size: 20, weight: 600, lineHeight: 28, letterSpacing: 0), Black: #191D23, Gray/04: #E4E7EB, Shadow 01: Effect(type: DROP_SHADOW, color: #4C67641A, offset: (0, 20), radius: 25, spread: 0), Special/Main BG: #F4F5F7.

## Tool response block 5

Images and SVGs will be stored as constants, e.g. const image = '[illustrative-asset-identifier-not-a-captured-resource]'. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.
