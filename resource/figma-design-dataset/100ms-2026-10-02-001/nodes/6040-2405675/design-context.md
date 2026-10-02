const assetPathPrefix = "../../assets";
const imgStateOff = "../../assets/4da918fbf8f34d5403358d16493e4e3147af9f875bdef0382c7128c9e1bcb2ed.svg";
const imgStateOn = "../../assets/4d76f17ed5fae648d60675c2d17428a5c7c52caeac72163487757cb5b4bd943d.svg";
const imgStateOnOutlined = "../../assets/0a2f54033e23be0854f7cf3eb7b01c3b20641bc928fca784afe651216bf2ad2e.svg";
const imgStateIndeterminate = "../../assets/8e8088dc3eba8f62879a5f22bcad3710a01f3e1c87b5c9a7f371cb26a270f9d6.svg";

type CheckboxProps = {
  className?: string;
  state?: "Off" | "On" | "Indeterminate" | "On Outlined";
};

function Checkbox({ className, state = "Off" }: CheckboxProps) {
  if (state === "On") {
    return (
      <button className={className || "block cursor-pointer relative size-[24px]"} data-node-id="6012:265369" data-name="State=On">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgStateOn} />
      </button>
    );
  }
  if (state === "On Outlined") {
    return (
      <div className={className || "relative size-[24px]"} data-node-id="6012:265373" data-name="State=On Outlined">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgStateOnOutlined} />
      </div>
    );
  }
  if (state === "Indeterminate") {
    return (
      <div className={className || "relative size-[24px]"} data-node-id="6012:265375" data-name="State=Indeterminate">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgStateIndeterminate} />
      </div>
    );
  }
  return (
    <button className={className || "block cursor-pointer relative size-[24px]"} data-node-id="6012:265367" data-name="State=Off">
      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgStateOff} />
    </button>
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

export default function Checkbox1() {
  return (
    <div className="content-stretch flex flex-col items-start relative size-full" data-node-id="6040:2405675" data-name="Checkbox">
      <FigmaFileHeader className="bg-[#131313] border-b-4 border-black border-solid content-stretch flex flex-col gap-[16px] items-start p-[64px] relative shrink-0 w-full" description="Allows to select one or more options from a number of choices" header="COMPONENTS" title="Checkbox" />
      <div className="bg-[#131313] h-[416px] relative shrink-0 w-[463px]" data-node-id="6040:2405674" data-name="Checkbox">
        <div className="absolute h-[288px] left-[139px] top-[64px] w-[163px]" data-node-id="6012:265347" data-name>
          <div className="absolute border border-[#9747ff] border-dashed content-stretch flex flex-col items-end left-[91px] rounded-[5px] top-0" data-node-id="6012:265348" data-name="Instances">
            <div className="content-stretch flex h-[72px] items-center relative shrink-0" data-node-id="6012:265349" data-name="Row">
              <div className="border-[#9747ff] border-b border-dashed h-full relative shrink-0 w-[72px]" data-node-id="6012:265350" data-name="Instance" />
            </div>
            <div className="content-stretch flex h-[72px] items-center relative shrink-0" data-node-id="6012:265351" data-name="Row">
              <div className="border-[#9747ff] border-b border-dashed h-full relative shrink-0 w-[72px]" data-node-id="6012:265352" data-name="Instance" />
            </div>
            <div className="content-stretch flex h-[72px] items-center relative shrink-0" data-node-id="6012:265353" data-name="Row">
              <div className="border-[#9747ff] border-b border-dashed h-full relative shrink-0 w-[72px]" data-node-id="6012:265354" data-name="Instance" />
            </div>
            <div className="content-stretch flex h-[72px] items-center relative shrink-0" data-node-id="6012:265355" data-name="Row">
              <div className="h-full relative shrink-0 w-[72px]" data-node-id="6012:265356" data-name="Instance" />
            </div>
          </div>
          <div className="absolute contents left-0 top-[10px]" data-node-id="6012:265357" data-name="Labels">
            <div className="absolute content-stretch flex h-[52px] items-center justify-end left-[25px] overflow-clip pr-[5px] top-[10px]" data-node-id="6012:265358" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6012:265359">
                State: Off
              </p>
            </div>
            <div className="absolute content-stretch flex h-[52px] items-center justify-end left-[27px] overflow-clip pr-[5px] top-[82px]" data-node-id="6012:265360" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6012:265361">
                State: On
              </p>
            </div>
            <div className="absolute content-stretch flex h-[52px] items-center justify-end left-0 overflow-clip pr-[5px] top-[154px]" data-node-id="6012:265362" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6012:265363">
                Indeterminate
              </p>
            </div>
            <div className="absolute content-stretch flex h-[52px] items-center justify-end left-[12px] overflow-clip pr-[5px] top-[226px]" data-node-id="6012:265364" data-name="Label">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[normal] not-italic relative shrink-0 text-[#9747ff] text-[12px] whitespace-nowrap" data-node-id="6012:265365">
                On Outlined
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

Images and SVGs will be stored as constants, e.g. const image = `${assetPathPrefix}/<asset file name>`, where assetPathPrefix is declared once at the top of the code and every asset URL interpolates it. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.
