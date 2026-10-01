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
const imgClarityNotificationSolidBadged = "../../assets/sha256-3f70d13a30dd8ed845438488f6e7ae2a8372b9de03d3ea505dc32e912a1826c4.svg";

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

export default function Component1064RemoveAndConfirmAccountDeletion() {
  return (
    <div className="content-stretch flex items-start relative size-full" data-node-id="2798:2356" data-name="106.4 Remove and Confirm Account Deletion">
      <div className="bg-[#191919] content-stretch flex flex-col gap-[228px] items-start px-[28px] py-[48px] relative shrink-0" data-node-id="2798:2357" data-name="Nav bar">
        <div className="content-stretch flex flex-col gap-[40px] items-start relative shrink-0" data-node-id="I2798:2357;411:6376" data-name="Logo & Menu">
          <p className="[word-break:break-word] font-['Poppins:Bold'] leading-[0] not-italic relative shrink-0 text-[0px] text-center text-white tracking-[1.92px] w-[224px]" data-node-id="I2798:2357;411:6377">
            <span className="font-['Poppins:ExtraBold'] leading-[32px] text-[24px]">FINE</span>
            <span className="font-['Poppins:Medium'] leading-[32px] text-[24px]">bank.</span>
            <span className="font-['Poppins:ExtraBold'] leading-[32px] text-[24px]">IO</span>
          </p>
          <div className="content-stretch flex flex-col gap-[16px] items-start relative shrink-0" data-node-id="I2798:2357;411:6378" data-name="Menu">
            <div className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2357;411:6379" data-name="Menu">
              <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2357;411:6379;2:118" data-name="Menu/Overview">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgMenuOverview1} />
              </div>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-[rgba(255,255,255,0.7)] w-[156px]" data-node-id="I2798:2357;411:6379;2:119">
                Overview
              </p>
            </div>
            <div className="bg-[#299d91] content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2357;411:6380" data-name="Menu">
              <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2357;411:6380;12:351" data-name="wallet">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgWallet} />
              </div>
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-white w-[156px]" data-node-id="I2798:2357;411:6380;2:125">
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
        <div className="content-stretch flex flex-col gap-[44px] items-start relative shrink-0" data-node-id="I2798:2357;411:6386" data-name="Footer">
          <div className="bg-[rgba(255,255,255,0.08)] content-stretch flex gap-[12px] items-center opacity-75 px-[16px] py-[12px] relative rounded-[4px] shrink-0" data-node-id="I2798:2357;411:6387" data-name="Logout Button">
            <div className="content-stretch flex items-center relative shrink-0 size-[24px]" data-node-id="I2798:2357;411:6387;13:631" data-name="Icon">
              <div className="relative shrink-0 size-[20px]" data-node-id="I2798:2357;411:6387;13:631;13:626" data-name="Logout">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLogout} />
              </div>
            </div>
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[24px] not-italic relative shrink-0 text-[16px] text-white w-[156px]" data-node-id="I2798:2357;411:6387;13:638">
              Logout
            </p>
          </div>
          <div className="border-[rgba(255,255,255,0.08)] border-solid border-t content-stretch flex gap-[32px] items-center py-[32px] relative shrink-0" data-node-id="I2798:2357;411:6388" data-name="Profile">
            <div className="content-stretch flex gap-[16px] items-center relative shrink-0" data-node-id="I2798:2357;411:6388;403:5380" data-name="Name & Picture">
              <div className="relative shrink-0 size-[32px]" data-node-id="I2798:2357;411:6388;403:5381" data-name="Image">
                <img alt="" className="absolute block inset-0 max-w-none size-full" height="32" src={imgImage} width="32" />
              </div>
              <div className="[word-break:break-word] content-stretch flex flex-col items-start not-italic relative shrink-0" data-node-id="I2798:2357;411:6388;403:5382" data-name="Name">
                <p className="font-['Inter:Semi_Bold'] font-semibold leading-[24px] relative shrink-0 text-[16px] text-white w-[140px]" data-node-id="I2798:2357;411:6388;403:5383">
                  Tanzir Rahman
                </p>
                <p className="font-['Inter:Regular'] font-normal leading-[16px] relative shrink-0 text-[12px] text-[rgba(255,255,255,0.7)] whitespace-nowrap" data-node-id="I2798:2357;411:6388;403:5384">
                  View profile
                </p>
              </div>
            </div>
            <div className="h-[20px] relative shrink-0 w-[4px]" data-node-id="I2798:2357;411:6388;403:5385" data-name="Icon">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon} />
            </div>
          </div>
        </div>
      </div>
      <div className="content-stretch flex flex-[1_0_0] flex-col items-start min-w-px relative" data-node-id="2798:2358" data-name="Main Content Pane">
        <div className="border-[#e8e8e8] border-b border-solid content-stretch flex items-center justify-between pl-[24px] pr-[32px] py-[20px] relative shrink-0 w-full" data-node-id="2798:2359" data-name="Header">
          <div className="content-stretch flex gap-[24px] items-center relative shrink-0" data-node-id="I2798:2359;411:6047" data-name="Header">
            <p className="[word-break:break-word] font-['Inter:Bold'] font-bold leading-[28px] not-italic relative shrink-0 text-[#191919] text-[24px] w-[140px]" data-node-id="I2798:2359;411:6048">
              Remove
              <br aria-hidden />
              Account
            </p>
            <div className="content-stretch flex gap-[4px] items-center relative shrink-0" data-node-id="I2798:2359;411:6049" data-name="Date">
              <div className="relative shrink-0 size-[24px]" data-node-id="I2798:2359;411:6050" data-name="chevrons-right">
                <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgChevronsRight} />
              </div>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[#9f9f9f] text-[14px] whitespace-nowrap" data-node-id="I2798:2359;411:6053">
                May 19, 2023
              </p>
            </div>
          </div>
          <div className="content-stretch flex gap-[40px] items-center relative shrink-0" data-node-id="I2798:2359;411:6054" data-name="Search">
            <div className="content-stretch flex items-center relative shrink-0" data-node-id="I2798:2359;411:6055" data-name="Notification icon">
              <div className="grid-cols-[max-content] grid-rows-[max-content] inline-grid leading-[0] place-items-start relative shrink-0" data-node-id="I2798:2359;411:6055;2:622">
                <div className="col-1 ml-0 mt-0 relative row-1 size-[24px]" data-node-id="I2798:2359;411:6055;2:623" data-name="clarity:notification-solid-badged">
                  <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgClarityNotificationSolidBadged} />
                </div>
              </div>
            </div>
            <div className="bg-white content-stretch drop-shadow-[0px_26px_13px_rgba(106,22,58,0.04)] flex gap-[170px] items-start pl-[32px] pr-[24px] py-[12px] relative rounded-[12px] shrink-0" data-node-id="I2798:2359;411:6056" data-name="Search">
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#9f9f9f] text-[16px] w-[102px]" data-node-id="I2798:2359;411:6056;404:5259">
                Search here
              </p>
              <Search className="relative shrink-0 size-[24px]" />
            </div>
          </div>
        </div>
        <div className="bg-[#f4f5f7] content-stretch flex flex-col h-[928px] items-center justify-center px-[40px] py-[32px] relative shrink-0 w-full" data-node-id="2798:2360" data-name="Content Inner">
          <div className="bg-white content-stretch drop-shadow-[0px_20px_12.5px_rgba(76,103,100,0.1)] flex flex-col gap-[32px] items-center justify-center p-[48px] relative rounded-[16px] shrink-0 w-[560px]" data-node-id="2798:2361" data-name="Delete Confirmation Card">
            <div className="bg-[rgba(242,51,51,0.1)] content-stretch flex items-center justify-center overflow-clip relative rounded-[32px] shrink-0 size-[64px]" data-node-id="2798:2362" data-name="Warning Icon Container">
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[normal] not-italic relative shrink-0 text-[#e53333] text-[32px] text-center whitespace-nowrap" data-node-id="2798:2363">
                ⚠
              </p>
            </div>
            <p className="[word-break:break-word] font-['Inter:Bold'] font-bold leading-[normal] min-w-full not-italic relative shrink-0 text-[#191919] text-[22px] text-center w-[min-content]" data-node-id="2798:2364">
              Confirm Account Deletion
            </p>
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[22px] min-w-full not-italic relative shrink-0 text-[#595959] text-[14px] text-center w-[min-content]" data-node-id="2798:2365">
              WARNING: Are you sure you want to delete the Vietcombank - 3123 account? This action will PERMANENTLY delete the account and ALL related transactions.
            </p>
            <div className="content-stretch flex gap-[16px] items-center justify-center overflow-clip relative shrink-0 w-full" data-node-id="2798:2366" data-name="Buttons">
              <div className="bg-[#ebedf0] border border-[#ccd1d6] border-solid content-stretch flex flex-[1_0_0] items-center justify-center min-w-px overflow-clip px-[32px] py-[12px] relative rounded-[4px]" data-node-id="2798:2367" data-name="Cancel Button">
                <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Semi_Bold'] font-semibold leading-[normal] min-w-px not-italic relative text-[#333] text-[14px] text-center" data-node-id="2798:2368">
                  Cancel
                </p>
              </div>
              <div className="bg-[#d92e2e] content-stretch flex flex-[1_0_0] items-center justify-center min-w-px overflow-clip px-[32px] py-[12px] relative rounded-[4px]" data-node-id="2798:2369" data-name="Confirm Delete Button">
                <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Semi_Bold'] font-semibold leading-[normal] min-w-px not-italic relative text-[14px] text-center text-white" data-node-id="2798:2370">
                  Confirm Delete
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

SUPER CRITICAL: The generated React+Tailwind code MUST be converted to match the target project's technology stack and styling system.
1. Analyze the target codebase to identify: technology stack, styling approach, component patterns, and design tokens
2. Convert React syntax to the target framework/library
3. Transform all Tailwind classes to the target styling system while preserving exact visual design
4. Follow the project's existing patterns and conventions
DO NOT install any Tailwind as a dependency unless the user instructs you to do so.


Node ids have been added to the code as data attributes, e.g. `data-node-id="1:2"`.

These styles are contained in the design: White: #FFFFFF, Special/BG2: #FFFFFF, Regular 16-24: Font(family: "Inter", style: Regular, size: 16, weight: 400, lineHeight: 24, letterSpacing: 0), Semibold 16-24: Font(family: "Inter", style: Semi Bold, size: 16, weight: 600, lineHeight: 24, letterSpacing: 0), Primary color: #299D91, Special/BG3: #FFFFFF, Regular 12-16: Font(family: "Inter", style: Regular, size: 12, weight: 400, lineHeight: 16, letterSpacing: 0), Default Black: #191919, Bold 24-28: Font(family: "Inter", style: Bold, size: 24, weight: 700, lineHeight: 28, letterSpacing: 0), Gray/03: #9F9F9F, Regular 14-20: Font(family: "Inter", style: Regular, size: 14, weight: 400, lineHeight: 20, letterSpacing: 0), Gray/01: #666666, Secondary: #525256, Gray/05: #E8E8E8, Shadow 01: Effect(type: DROP_SHADOW, color: #4C67641A, offset: (0, 20), radius: 25, spread: 0), Special/Main BG: #F4F5F7.

Images and SVGs will be stored as constants, e.g. const image = '../../assets/<example>'. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.
