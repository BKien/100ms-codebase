const assetPathPrefix = "../../assets";
const imgIcon = "../../assets/904403123f38e29ff80b466068ca722fb006a8074e0a320692d2c69e0fff048c.svg";
const imgOutlineCross = "../../assets/418f6f1f574e6f41450e01b2472b0dcf84ec078866c813e1f3df9585496ee8cf.svg";
const imgIcon1 = "../../assets/904403123f38e29ff80b466068ca722fb006a8074e0a320692d2c69e0fff048c.svg";
const imgOutlineCross1 = "../../assets/418f6f1f574e6f41450e01b2472b0dcf84ec078866c813e1f3df9585496ee8cf.svg";

type ChipProps = {
  className?: string;
  closeable?: boolean;
  icon?: React.ReactNode | null;
  showIcon?: boolean;
  state?: "Default" | "Hover";
  text?: string;
  type?: "Primary" | "Secondary";
};

function Chip({ className, closeable = true, icon = null, showIcon = true, state = "Default", text = "Text", type = "Primary" }: ChipProps) {
  const isPrimary = type === "Primary";
  const isPrimaryAndDefault = type === "Primary" && state === "Default";
  const isPrimaryAndHover = type === "Primary" && state === "Hover";
  const isSecondary = type === "Secondary";
  const isSecondaryAndHover = type === "Secondary" && state === "Hover";
  return (
    <div className={className || `${String.raw`content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] `}${isPrimaryAndHover ? String.raw`bg-[var(--primary\/bright,#538dff)]` : isPrimaryAndDefault ? String.raw`bg-[var(--primary\/default,#2572ed)]` : isSecondaryAndHover ? String.raw`bg-[var(--secondary\/bright,#70778b)]` : String.raw`bg-[var(--secondary\/default,#444954)]`}`} id={isPrimaryAndHover ? "node-6012_265251" : isPrimaryAndDefault ? "node-6012_265246" : isSecondaryAndHover ? "node-6012_265241" : "node-6012_265236"}>
      {isSecondary &&
        showIcon &&
        (icon || (
          <div className="relative shrink-0 size-[24px]" data-node-id="6012:265237" data-name="Icon">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon} />
          </div>
        ))}
      {isSecondary && (
        <div className="content-stretch flex items-start px-[8px] relative shrink-0" id={isSecondaryAndHover ? "node-6012_265243" : "node-6012_265238"} data-name="Text Container">
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-secondary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="6012:265239">
            {text}
          </p>
        </div>
      )}
      {isSecondary && closeable && (
        <div className="relative shrink-0 size-[20px]" data-node-id="6012:265240" data-name="Outline/Cross">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgOutlineCross} />
        </div>
      )}
      {isPrimary &&
        showIcon &&
        (icon || (
          <div className="relative shrink-0 size-[24px]" data-node-id="6012:265247" data-name="Icon">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon1} />
          </div>
        ))}
      {isPrimary && (
        <div className="content-stretch flex items-start px-[8px] relative shrink-0" id={isPrimaryAndHover ? "node-6012_265253" : "node-6012_265248"} data-name="Text Container">
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-primary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="6012:265249">
            {text}
          </p>
        </div>
      )}
      {isPrimary && closeable && (
        <div className="relative shrink-0 size-[20px]" data-node-id="6012:265250" data-name="Outline/Cross">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgOutlineCross1} />
        </div>
      )}
    </div>
  );
}

type FigmaFileHeaderProps = {
  className?: string;
  description?: string;
  header?: string;
  title?: string;
};

function FigmaFileHeader({ className, description = "Description text dolor sit incididunt, adipisicing tempor, tempor labore dolore magna aliqua.", header = "FOUNDATION", title = "Title" }: FigmaFileHeaderProps) {
  return (
    <div className={className || "bg-[#131313] border-b-4 border-black border-solid content-stretch flex flex-col gap-[16px] items-start p-[64px] relative w-[1910px]"} data-node-id="4703:103124" data-name="Figma File Header">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Semi_Bold'] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[20px] text-[rgba(255,255,255,0.6)] tracking-[1.6px] uppercase whitespace-nowrap" data-node-id="4703:103125">
        <p className="leading-[1.2]">{header}</p>
      </div>
      <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="4703:103126" data-name="Heading and supporting text">
        <div className="content-stretch flex gap-[24px] items-center relative shrink-0 w-full" data-node-id="4703:103127" data-name="Heading">
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[72px] not-italic relative shrink-0 text-[56px] text-[rgba(255,255,255,0.9)] tracking-[-1.12px] whitespace-nowrap" data-node-id="4703:103128">
            {title}
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.2] not-italic relative shrink-0 text-[20px] text-[rgba(255,255,255,0.4)] w-full" data-node-id="4703:103131">
          {description}
        </p>
      </div>
    </div>
  );
}

export default function Chip1() {
  return (
    <div className="content-stretch flex flex-col items-center relative size-full" data-node-id="6040:2407189" data-name="Chip">
      <FigmaFileHeader className="bg-[#131313] border-b-4 border-black border-solid content-stretch flex flex-col gap-[16px] items-start p-[64px] relative shrink-0 w-full" description="Chips are compact elements that represent an input, attribute, or action." header="component" title="Chip" />
      <div className="bg-[#131313] h-[529px] relative shrink-0 w-[920px]" data-node-id="6040:2407188" data-name="Chip">
        <div className="absolute h-[419px] left-[52px] top-[55px] w-[816px]" data-node-id="6040:2406477" data-name>
          <div className="absolute border border-[#9747ff] border-dashed content-stretch flex flex-col items-end left-[196px] rounded-[5px] top-[67px]" data-node-id="6040:2406479" data-name="Instances">
            <div className="content-stretch flex h-[88px] items-center relative shrink-0" data-node-id="6040:2406493" data-name="Row">
              <div className="border-[#9747ff] border-b border-dashed border-r h-full relative shrink-0 w-[160px]" data-node-id="6040:2406494" data-name="Instance" />
              <div className="border-[#9747ff] border-b border-dashed border-r h-full relative shrink-0 w-[160px]" data-node-id="6040:2406507" data-name="Instance" />
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-b border-dashed border-r content-stretch flex h-full items-center justify-center relative shrink-0 w-[140px]" data-node-id="6040:2406520" data-name="Instance">
                <div className="bg-[var(--primary\/default,#2572ed)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406521" data-name="Chip">
                  <div className="relative shrink-0 size-[24px]" data-node-id="I6040:2406521;6012:265247" data-name="Icon">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon1} />
                  </div>
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406521;6012:265248" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-primary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406521;6012:265249">
                      Text
                    </p>
                  </div>
                </div>
              </div>
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-b border-dashed content-stretch flex h-full items-center justify-center relative shrink-0 w-[160px]" data-node-id="6040:2406544" data-name="Instance">
                <div className="bg-[var(--primary\/bright,#538dff)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406545" data-name="Chip">
                  <div className="relative shrink-0 size-[24px]" data-node-id="I6040:2406545;6012:265252" data-name="Icon">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon1} />
                  </div>
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406545;6012:265253" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-primary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406545;6012:265254">
                      Text
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div className="content-stretch flex h-[88px] items-center relative shrink-0" data-node-id="6040:2406557" data-name="Row">
              <div className="border-[#9747ff] border-b border-dashed border-r h-full relative shrink-0 w-[160px]" data-node-id="6040:2406558" data-name="Instance" />
              <div className="border-[#9747ff] border-b border-dashed border-r h-full relative shrink-0 w-[160px]" data-node-id="6040:2406579" data-name="Instance" />
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-b border-dashed border-r content-stretch flex h-full items-center justify-center relative shrink-0 w-[140px]" data-node-id="6040:2406603" data-name="Instance">
                <div className="bg-[var(--secondary\/default,#444954)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406604" data-name="Chip">
                  <div className="relative shrink-0 size-[24px]" data-node-id="I6040:2406604;6012:265237" data-name="Icon">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon} />
                  </div>
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406604;6012:265238" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-secondary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406604;6012:265239">
                      Text
                    </p>
                  </div>
                </div>
              </div>
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-b border-dashed content-stretch flex h-full items-center justify-center relative shrink-0 w-[160px]" data-node-id="6040:2406627" data-name="Instance">
                <div className="bg-[var(--secondary\/bright,#70778b)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406628" data-name="Chip">
                  <div className="relative shrink-0 size-[24px]" data-node-id="I6040:2406628;6012:265242" data-name="Icon">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon} />
                  </div>
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406628;6012:265243" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-secondary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406628;6012:265244">
                      Text
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div className="content-stretch flex h-[88px] items-center relative shrink-0" data-node-id="6040:2406648" data-name="Row">
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-b border-dashed border-r content-stretch flex h-full items-center justify-center relative shrink-0 w-[160px]" data-node-id="6040:2406649" data-name="Instance">
                <div className="bg-[var(--primary\/default,#2572ed)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406650" data-name="Chip">
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406650;6012:265248" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-primary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406650;6012:265249">
                      Text
                    </p>
                  </div>
                  <div className="relative shrink-0 size-[20px]" data-node-id="I6040:2406650;6012:265250" data-name="Outline/Cross">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgOutlineCross1} />
                  </div>
                </div>
              </div>
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-b border-dashed border-r content-stretch flex h-full items-center justify-center relative shrink-0 w-[160px]" data-node-id="6040:2406670" data-name="Instance">
                <div className="bg-[var(--primary\/bright,#538dff)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406671" data-name="Chip">
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406671;6012:265253" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-primary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406671;6012:265254">
                      Text
                    </p>
                  </div>
                  <div className="relative shrink-0 size-[20px]" data-node-id="I6040:2406671;6012:265255" data-name="Outline/Cross">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgOutlineCross1} />
                  </div>
                </div>
              </div>
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-b border-dashed border-r content-stretch flex h-full items-center justify-center relative shrink-0 w-[140px]" data-node-id="6040:2406683" data-name="Instance">
                <div className="bg-[var(--primary\/default,#2572ed)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406684" data-name="Chip">
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406684;6012:265248" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-primary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406684;6012:265249">
                      Text
                    </p>
                  </div>
                </div>
              </div>
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-b border-dashed content-stretch flex h-full items-center justify-center relative shrink-0 w-[160px]" data-node-id="6040:2406703" data-name="Instance">
                <div className="bg-[var(--primary\/bright,#538dff)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406704" data-name="Chip">
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406704;6012:265253" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-primary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406704;6012:265254">
                      Text
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div className="content-stretch flex h-[88px] items-center relative shrink-0" data-node-id="6040:2406716" data-name="Row">
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-dashed border-r content-stretch flex h-full items-center justify-center relative shrink-0 w-[160px]" data-node-id="6040:2406717" data-name="Instance">
                <div className="bg-[var(--secondary\/default,#444954)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406718" data-name="Chip">
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406718;6012:265238" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-secondary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406718;6012:265239">
                      Text
                    </p>
                  </div>
                  <div className="relative shrink-0 size-[20px]" data-node-id="I6040:2406718;6012:265240" data-name="Outline/Cross">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgOutlineCross} />
                  </div>
                </div>
              </div>
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-dashed border-r content-stretch flex h-full items-center justify-center relative shrink-0 w-[160px]" data-node-id="6040:2406734" data-name="Instance">
                <div className="bg-[var(--secondary\/bright,#70778b)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406735" data-name="Chip">
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406735;6012:265243" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-secondary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406735;6012:265244">
                      Text
                    </p>
                  </div>
                  <div className="relative shrink-0 size-[20px]" data-node-id="I6040:2406735;6012:265245" data-name="Outline/Cross">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgOutlineCross} />
                  </div>
                </div>
              </div>
              <div className="bg-[rgba(151,71,255,0.03)] border-[#9747ff] border-dashed border-r content-stretch flex h-full items-center justify-center relative shrink-0 w-[140px]" data-node-id="6040:2406754" data-name="Instance">
                <div className="bg-[var(--secondary\/default,#444954)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406755" data-name="Chip">
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406755;6012:265238" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-secondary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406755;6012:265239">
                      Text
                    </p>
                  </div>
                </div>
              </div>
              <div className="bg-[rgba(151,71,255,0.03)] content-stretch flex h-full items-center justify-center relative shrink-0 w-[160px]" data-node-id="6040:2406774" data-name="Instance">
                <div className="bg-[var(--secondary\/bright,#70778b)] content-stretch flex items-center justify-center p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" data-node-id="6040:2406775" data-name="Chip">
                  <div className="content-stretch flex items-start px-[8px] relative shrink-0" data-node-id="I6040:2406775;6012:265243" data-name="Text Container">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-[color:var(--on-secondary\/high,white)] tracking-[0.5px] whitespace-nowrap" data-node-id="I6040:2406775;6012:265244">
                      Text
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="absolute contents left-0 top-0" data-node-id="6040:2407007" data-name="Labels">
            <div className="absolute content-stretch flex gap-[8px] h-[156px] items-center justify-end left-[5px] overflow-clip top-[77px]" data-node-id="6040:2406793" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406794">
                Show Icon: True
              </p>
              <div className="border-[#9747ff] border-b border-l border-solid border-t h-full relative rounded-bl-[5px] rounded-tl-[5px] shrink-0 w-[14px]" data-node-id="6040:2406795" data-name="Bracket" />
            </div>
            <div className="absolute content-stretch flex gap-[8px] h-[156px] items-center justify-end left-0 overflow-clip top-[253px]" data-node-id="6040:2406797" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406798">
                Show Icon: False
              </p>
              <div className="border-[#9747ff] border-b border-l border-solid border-t h-full relative rounded-bl-[5px] rounded-tl-[5px] shrink-0 w-[14px]" data-node-id="6040:2406799" data-name="Bracket" />
            </div>
            <div className="absolute content-stretch flex h-[68px] items-center justify-end left-[141px] overflow-clip pr-[5px] top-[77px]" data-node-id="6040:2406802" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406803">
                Primary
              </p>
            </div>
            <div className="absolute content-stretch flex h-[68px] items-center justify-end left-[124px] overflow-clip pr-[5px] top-[165px]" data-node-id="6040:2406805" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406806">
                Secondary
              </p>
            </div>
            <div className="absolute content-stretch flex h-[68px] items-center justify-end left-[141px] overflow-clip pr-[5px] top-[253px]" data-node-id="6040:2406808" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406809">
                Primary
              </p>
            </div>
            <div className="absolute content-stretch flex h-[68px] items-center justify-end left-[124px] overflow-clip pr-[5px] top-[341px]" data-node-id="6040:2406811" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406812">
                Secondary
              </p>
            </div>
            <div className="absolute content-stretch flex flex-col gap-[8px] items-center justify-end left-[206px] overflow-clip top-0 w-[300px]" data-node-id="6040:2406815" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406816">
                Closeable: True
              </p>
              <div className="border-[#9747ff] border-l border-r border-solid border-t h-[14px] relative rounded-tl-[5px] rounded-tr-[5px] shrink-0 w-full" data-node-id="6040:2406817" data-name="Bracket" />
            </div>
            <div className="absolute content-stretch flex flex-col gap-[8px] items-center justify-end left-[526px] overflow-clip top-0 w-[280px]" data-node-id="6040:2406819" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406820">
                Closeable: False
              </p>
              <div className="border-[#9747ff] border-l border-r border-solid border-t h-[14px] relative rounded-tl-[5px] rounded-tr-[5px] shrink-0 w-full" data-node-id="6040:2406821" data-name="Bracket" />
            </div>
            <div className="absolute content-stretch flex flex-col items-center justify-end left-[206px] overflow-clip pb-[5px] top-[42px] w-[140px]" data-node-id="6040:2406824" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406825">
                Default
              </p>
            </div>
            <div className="absolute content-stretch flex flex-col items-center justify-end left-[366px] overflow-clip pb-[5px] top-[42px] w-[140px]" data-node-id="6040:2406827" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406828">
                Hover
              </p>
            </div>
            <div className="absolute content-stretch flex flex-col items-center justify-end left-[526px] overflow-clip pb-[5px] top-[42px] w-[120px]" data-node-id="6040:2406830" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406831">
                Default
              </p>
            </div>
            <div className="absolute content-stretch flex flex-col items-center justify-end left-[666px] overflow-clip pb-[5px] top-[42px] w-[140px]" data-node-id="6040:2406833" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6040:2406834">
                Hover
              </p>
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

These styles are contained in the design: Desktop/Button-Semibold-16px: Font(family: "Inter", style: Semi Bold, size: 16, weight: 600, lineHeight: 24, letterSpacing: 0.5).

Images and SVGs will be stored as constants, e.g. const image = `${assetPathPrefix}/<asset file name>`, where assetPathPrefix is declared once at the top of the code and every asset URL interpolates it. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.
