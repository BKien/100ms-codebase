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

export default function FigmaFileHeader1() {
  return <FigmaFileHeader className="bg-[#131313] border-b-4 border-black border-solid content-stretch flex flex-col gap-[16px] items-start p-[64px] relative size-full" description="Open source icons designed to make your product attractive, visually consistent and simply beautiful. Icons courtesy of Lucide." title="Icons" />;
}

SUPER CRITICAL: The generated React+Tailwind code MUST be converted to match the target project's technology stack and styling system.
1. Analyze the target codebase to identify: technology stack, styling approach, component patterns, and design tokens
2. Convert React syntax to the target framework/library
3. Transform all Tailwind classes to the target styling system while preserving exact visual design
4. Follow the project's existing patterns and conventions
DO NOT install any Tailwind as a dependency unless the user instructs you to do so.


Node ids have been added to the code as data attributes, e.g. `data-node-id="1:2"`.

Images and SVGs will be stored as constants, e.g. const image = `${assetPathPrefix}/<asset file name>`, where assetPathPrefix is declared once at the top of the code and every asset URL interpolates it. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.
