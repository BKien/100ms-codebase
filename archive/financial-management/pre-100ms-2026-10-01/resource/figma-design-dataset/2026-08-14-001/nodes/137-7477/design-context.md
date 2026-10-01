## Figma response 1

const imgTick = "assets/context-001.svg";
const imgVector = "assets/context-002.svg";
const imgVector1 = "assets/context-003.svg";
const imgLine10 = "assets/context-004.svg";
const imgClipPathGroup = "assets/context-005.svg";
const imgClipPathGroup1 = "assets/context-006.svg";
const imgClipPathGroup2 = "assets/context-007.svg";
const imgClipPathGroup3 = "assets/context-008.svg";

type ButtonPrimaryProps = {
  className?: string;
  active?: "Yes";
};

function ButtonPrimary({ className, active = "Yes" }: ButtonPrimaryProps) {
  return (
    <div className={className || "bg-[#299d91] content-stretch flex h-[48px] items-center justify-center px-[12px] py-[16px] relative rounded-[4px] w-[400px]"} data-node-id="402:5240">
      <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-center text-white w-[160px]" data-node-id="402:5241">
        Login
      </p>
    </div>
  );
}

type RemindMeProps = {
  className?: string;
  active?: "Yes";
};

function RemindMe({ className, active = "Yes" }: RemindMeProps) {
  return (
    <div className={className || "content-stretch flex gap-[16px] items-center relative"} data-node-id="402:5227">
      <div className="relative shrink-0 size-[20px]" data-node-id="402:5228" data-name="Tick">
        <div className="absolute bg-[#299d91] inset-0 rounded-[2px]" data-node-id="I402:5228;73:526" data-name="fill" />
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgTick} />
      </div>
      <p className="[word-break:break-word] font-['Inter:Light'] font-light leading-[24px] not-italic relative shrink-0 text-[#191d23] text-[16px] w-[228px]" data-node-id="402:5229">
        Keep me signed in
      </p>
    </div>
  );
}

function IconEye({ className }: { className?: string }) {
  return (
    <div className={className || "overflow-clip relative size-[24px]"} data-node-id="402:5244" data-name="Icon/eye">
      <div className="absolute inset-[20.83%_8.33%]" data-node-id="402:5245" data-name="Vector">
        <div className="absolute inset-[-7.14%_-5%]">
          <img alt="" className="block max-w-none size-full" src={imgVector} />
        </div>
      </div>
      <div className="absolute inset-[37.5%]" data-node-id="402:5246" data-name="Vector">
        <div className="absolute inset-[-16.67%]">
          <img alt="" className="block max-w-none size-full" src={imgVector1} />
        </div>
      </div>
    </div>
  );
}

type InputProps = {
  className?: string;
  active?: boolean;
  type?: "Password" | "Name-Email";
};

function Input({ className, active = true, type = "Name-Email" }: InputProps) {
  const isNameEmailAndActive = type === "Name-Email" && active;
  const isPasswordAndNotActive = type === "Password" && !active;
  return (
    <div className={className || `border border-solid content-stretch flex h-[48px] items-start px-[16px] py-[12px] relative rounded-[8px] w-[400px] ${isNameEmailAndActive ? "border-[#4b5768]" : "border-[#d0d5dd] justify-between"}`} id={isNameEmailAndActive ? "node-402_5206" : "node-402_5192"}>
      <p className={`[word-break:break-word] font-["Inter:Regular"] font-normal h-[24px] not-italic relative shrink-0 ${isNameEmailAndActive ? "leading-[0] text-[#4b5768] text-[16px] w-[314px]" : "leading-[24px] text-[#999da3] text-[4px] tracking-[4px] w-[262px]"}`} id={isNameEmailAndActive ? "node-402_5207" : "node-402_5193"}>
        {isPasswordAndNotActive && "●●●●●●●●●●●●●●"}
        {isNameEmailAndActive && (
          <>
            <span className="leading-[22px]">johnd</span>
            <span className="leading-[22px]">oe@email.com</span>
          </>
        )}
      </p>
      {isPasswordAndNotActive && <IconEye className="overflow-clip relative shrink-0 size-[24px]" />}
    </div>
  );
}

export default function Component101Login() {
  return (
    <div className="bg-[#f4f5f7] relative size-full" data-node-id="137:7477" data-name="101. Login">
      <div className="absolute content-stretch flex flex-col gap-[40px] items-start left-[520px] top-[160px]" data-node-id="137:8302">
        <div className="content-stretch flex flex-col gap-[64px] items-center relative shrink-0" data-node-id="137:8063">
          <div className="content-stretch flex flex-col items-center relative shrink-0" data-node-id="137:8062">
            <p className="[word-break:break-word] font-['Poppins:Bold'] leading-[0] not-italic relative shrink-0 text-[#299d91] text-[0px] text-center tracking-[3.2px] whitespace-nowrap" data-node-id="137:7957">
              <span className="font-['Poppins:ExtraBold'] leading-[32px] text-[40px]">FINE</span>
              <span className="font-['Poppins:Medium'] leading-[32px] text-[40px]">bank.</span>
              <span className="font-['Poppins:ExtraBold'] leading-[32px] text-[40px]">IO</span>
            </p>
          </div>
          <div className="content-stretch flex flex-col gap-[24px] items-center relative shrink-0" data-node-id="137:8010" data-name="Input section">
            <div className="content-stretch flex flex-col gap-[32px] items-start relative shrink-0" data-node-id="137:8011" data-name="Login">
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0" data-node-id="137:8012" data-name="Input">
                <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="137:8013" data-name="Email">
                  <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[24px] leading-[24px] not-italic overflow-hidden relative shrink-0 text-[#191d23] text-[16px] text-ellipsis w-[342px] whitespace-nowrap" data-node-id="137:8014">
                    Email Address
                  </p>
                  <Input className="border border-[#4b5768] border-solid content-stretch flex h-[48px] items-start px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-[400px]" />
                </div>
                <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="137:8016" data-name="Password">
                  <div className="[word-break:break-word] content-stretch flex font-['Inter:Medium'] font-medium items-center justify-between not-italic relative shrink-0 w-[400px]" data-node-id="137:8017" data-name="Header">
                    <p className="h-[24px] leading-[24px] overflow-hidden relative shrink-0 text-[#191d23] text-[16px] text-ellipsis w-[160px] whitespace-nowrap" data-node-id="137:8018">
                      Password
                    </p>
                    <a className="block cursor-pointer leading-[0] relative shrink-0 text-[#299d91] text-[12px] text-right w-[162px]" data-node-id="137:8019">
                      <p className="leading-[16px]">Forgot Password?</p>
                    </a>
                  </div>
                  <Input active={false} className="border border-[#d0d5dd] border-solid content-stretch flex h-[48px] items-start justify-between px-[16px] py-[12px] relative rounded-[8px] shrink-0 w-[400px]" type="Password" />
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[16px] items-start relative shrink-0" data-node-id="137:8021" data-name="Button">
                <RemindMe className="content-stretch flex gap-[16px] items-center relative shrink-0" />
                <ButtonPrimary className="bg-[#299d91] content-stretch cursor-pointer flex h-[48px] items-center justify-center px-[12px] py-[16px] relative rounded-[4px] shrink-0 w-[400px]" />
              </div>
            </div>
            <div className="content-stretch flex flex-col items-center relative shrink-0" data-node-id="137:8024" data-name="Devider">
              <div className="-translate-x-1/2 absolute h-0 left-1/2 top-[18px] w-[342px]" data-node-id="137:8025">
                <div className="absolute inset-[-0.5px_0_0_0]">
                  <img alt="" className="block max-w-none size-full" src={imgLine10} />
                </div>
              </div>
              <div className="bg-[#f4f5f7] content-stretch flex items-start p-[8px] relative shrink-0" data-node-id="137:8026" data-name="Sign in with">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[#999da3] text-[14px] text-center w-[112px]" data-node-id="137:8027">
                  or sign in with
                </p>
              </div>
            </div>
            <div className="bg-[#e4e7eb] content-stretch flex gap-[16px] h-[48px] items-center justify-center px-[69px] py-[12px] relative rounded-[4px] shrink-0 w-[400px]" data-node-id="402:5501" data-name="Button/secondary">
              <div className="overflow-clip relative shrink-0 size-[24px]" data-node-id="I402:5501;402:5235" data-name="Google">
                <div className="absolute contents inset-[0_0.71%_0_1.56%]" data-node-id="I402:5501;402:5235;9:696" data-name="Group">
                  <div className="absolute inset-[0_0.71%_0_1.56%]" data-node-id="I402:5501;402:5235;9:697" data-name="Clip path group">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgClipPathGroup} />
                  </div>
                  <div className="absolute inset-[0_0.71%_0_1.56%]" data-node-id="I402:5501;402:5235;9:701" data-name="Clip path group">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgClipPathGroup1} />
                  </div>
                  <div className="absolute inset-[0_0.71%_0_1.56%]" data-node-id="I402:5501;402:5235;9:705" data-name="Clip path group">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgClipPathGroup2} />
                  </div>
                  <div className="absolute inset-[0_0.71%_0_1.56%]" data-node-id="I402:5501;402:5235;9:709" data-name="Clip path group">
                    <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgClipPathGroup3} />
                  </div>
                </div>
              </div>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[#4b5768] text-[16px] text-center whitespace-nowrap" data-node-id="I402:5501;402:5236">
                Continue with Google
              </p>
            </div>
          </div>
        </div>
        <a className="[word-break:break-word] block cursor-pointer font-['Inter:Semi_Bold'] font-semibold h-[24px] leading-[0] not-italic overflow-hidden relative shrink-0 text-[#299d91] text-[16px] text-center text-ellipsis w-[400px] whitespace-nowrap" data-node-id="137:8301">
          <p className="leading-[24px] overflow-hidden text-ellipsis">Create an account</p>
        </a>
      </div>
    </div>
  );
}

## Figma response 2

SUPER CRITICAL: The generated React+Tailwind code MUST be converted to match the target project's technology stack and styling system.
1. Analyze the target codebase to identify: technology stack, styling approach, component patterns, and design tokens
2. Convert React syntax to the target framework/library
3. Transform all Tailwind classes to the target styling system while preserving exact visual design
4. Follow the project's existing patterns and conventions
DO NOT install any Tailwind as a dependency unless the user instructs you to do so.


## Figma response 3

Node ids have been added to the code as data attributes, e.g. `data-node-id="1:2"`.

## Figma response 4

These styles are contained in the design: Primary color: #299D91, Black: #191D23, Medium 16-24: Font(family: "Inter", style: Medium, size: 16, weight: 500, lineHeight: 24, letterSpacing: 0), Gray/02: #4B5768, Gray/01: #999DA3, Gray/03: #D0D5DD, White: #FFFFFF, Light 16-24: Font(family: "Inter", style: Light, size: 16, weight: 300, lineHeight: 24, letterSpacing: 0), Semibold 16-24: Font(family: "Inter", style: Semi Bold, size: 16, weight: 600, lineHeight: 24, letterSpacing: 0), Regular 14-20: Font(family: "Inter", style: Regular, size: 14, weight: 400, lineHeight: 20, letterSpacing: 0), Special/Main BG: #F4F5F7, Special/Red: #E73D1C, Regular 16-24: Font(family: "Inter", style: Regular, size: 16, weight: 400, lineHeight: 24, letterSpacing: 0), Gray/04: #E4E7EB.

## Figma response 5

Images and SVGs will be stored as constants, e.g. const image = '<ephemeral-asset-example-removed>'. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.

