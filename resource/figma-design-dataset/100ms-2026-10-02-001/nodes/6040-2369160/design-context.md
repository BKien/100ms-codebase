const assetPathPrefix = "../../assets";
const imgOutlineLoaderSpinner = "../../assets/109ff52606a08021cf8e6e9b341bc5913c34ab0214823c9fe40d58e94d5c2513.svg";

function OutlineLoaderSpinner({ className }: { className?: string }) {
  return (
    <div className={className || "relative size-[24px]"} data-node-id="6013:634670" data-name="Outline/Loader,Spinner">
      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgOutlineLoaderSpinner} />
    </div>
  );
}

function LoadingIndicator({ className }: { className?: string }) {
  return (
    <div className={className || "relative size-[24px]"} data-node-id="6012:269305" data-name="_Loading Indicator">
      <OutlineLoaderSpinner className="-translate-x-1/2 -translate-y-1/2 absolute left-1/2 size-[24px] top-1/2" />
    </div>
  );
}

function FocusStroke({ className }: { className?: string }) {
  return (
    <div className={className || "h-[48px] relative w-[143px]"} data-node-id="6012:269303" data-name="_Focus Stroke">
      <div className="absolute border-4 border-[rgba(36,113,237,0.5)] border-solid inset-0 rounded-[var(--radius\/1,8px)]" data-node-id="6012:269304" data-name="Focus Stroke" />
    </div>
  );
}

type TooltipProps = {
  className?: string;
  description?: string;
};

function Tooltip({ className, description = "Audio" }: TooltipProps) {
  return (
    <div className={className || "bg-[var(--surface\\/default,#191b23)] border border-[var(--secondary\\/dim,#293042)] border-solid content-stretch flex items-start p-[var(--$2,8px)] relative rounded-[var(--radius\\/5,40px)]"} data-node-id="6012:269301" data-name="_Tooltip">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[16px] not-italic relative shrink-0 text-[12px] text-[color:var(--on-surface\/medium,#c5c6d0)] text-center tracking-[0.4px] whitespace-nowrap" data-node-id="6012:269302">
        {description}
      </p>
    </div>
  );
}

export default function Base() {
  return (
    <div className="content-stretch flex flex-col items-center relative size-full" data-node-id="6040:2369160" data-name="_Base">
      <div className="bg-[#131313] border-b-4 border-black border-solid content-stretch flex flex-col gap-[16px] items-start p-[64px] relative shrink-0 w-full" data-node-id="6012:269308" data-name="Figma File Header">
        <div className="[word-break:break-word] flex flex-col font-['Inter:Semi_Bold'] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[20px] text-[rgba(255,255,255,0.6)] tracking-[1.6px] uppercase whitespace-nowrap" data-node-id="I6012:269308;4703:103125">
          <p className="leading-[1.2]">Components</p>
        </div>
        <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="I6012:269308;4703:103126" data-name="Heading and supporting text">
          <div className="content-stretch flex gap-[24px] items-center relative shrink-0 w-full" data-node-id="I6012:269308;4703:103127" data-name="Heading">
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[72px] not-italic relative shrink-0 text-[56px] text-[rgba(255,255,255,0.9)] tracking-[-1.12px] whitespace-nowrap" data-node-id="I6012:269308;4703:103128">
              _Base
            </p>
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[30px] not-italic relative shrink-0 text-[20px] text-[rgba(255,255,255,0.4)] w-full" data-node-id="I6012:269308;4703:103131">
            Base components that are reused by button components
          </p>
        </div>
      </div>
      <div className="bg-[#131313] content-stretch flex gap-[52px] items-center p-[64px] relative shrink-0" data-node-id="6040:2369159" data-name="Unit">
        <Tooltip className="bg-[var(--surface\/default,#191b23)] border border-[var(--secondary\/dim,#293042)] border-solid content-stretch flex items-start p-[var(--$2,8px)] relative rounded-[var(--radius\/5,40px)] shrink-0" />
        <FocusStroke className="h-[48px] relative shrink-0 w-[143px]" />
        <LoadingIndicator className="relative shrink-0 size-[24px]" />
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

These styles are contained in the design: Desktop/Caption-Regular-12px: Font(family: "Inter", style: Regular, size: 12, weight: 400, lineHeight: 16, letterSpacing: 0.4000000059604645).

Images and SVGs will be stored as constants, e.g. const image = `${assetPathPrefix}/<asset file name>`, where assetPathPrefix is declared once at the top of the code and every asset URL interpolates it. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.
