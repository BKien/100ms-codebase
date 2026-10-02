function Divider({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--border\\/bright,#272a31)] h-px relative w-[473px]"} data-node-id="6012:271829" data-name="– Divider –">
      <div className="-translate-y-1/2 absolute h-px left-0 opacity-10 right-0 top-1/2" data-node-id="6012:271828" data-name="➖Divider" />
    </div>
  );
}

export default function Divider1() {
  return (
    <div className="content-stretch flex flex-col items-start relative size-full" data-node-id="6045:13847" data-name="Divider">
      <div className="bg-[#131313] border-b-4 border-black border-solid content-stretch flex flex-col gap-[16px] items-start p-[64px] relative shrink-0 w-full" data-node-id="6012:271818" data-name="Figma File Header">
        <div className="[word-break:break-word] flex flex-col font-['Inter:Semi_Bold'] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[20px] text-[rgba(255,255,255,0.6)] tracking-[1.6px] uppercase whitespace-nowrap" data-node-id="I6012:271818;4703:103125">
          <p className="leading-[1.2]">COMPONENTS</p>
        </div>
        <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="I6012:271818;4703:103126" data-name="Heading and supporting text">
          <div className="content-stretch flex gap-[24px] items-center relative shrink-0 w-full" data-node-id="I6012:271818;4703:103127" data-name="Heading">
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[72px] not-italic relative shrink-0 text-[56px] text-[rgba(255,255,255,0.9)] tracking-[-1.12px] whitespace-nowrap" data-node-id="I6012:271818;4703:103128">
              Divider
            </p>
          </div>
        </div>
      </div>
      <div className="bg-[#131313] h-[159px] relative shrink-0 w-[619px]" data-node-id="6045:13846" data-name="Unit">
        <Divider className="absolute flex inset-[49.69%_11.79%] items-center justify-center" />
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
