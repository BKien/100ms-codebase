const assetPathPrefix = "../../assets";
const imgIcon = "../../assets/5617a341b13fade245cdbd3ee05fc8ba63cc1c642a5584f8c403c14c5b6cc83a.svg";
const imgIcon1 = "../../assets/be27aa7e15ec11e0aa658ff1b7b1129385772382eef1b4c84542710d189cda78.svg";
const imgIcon2 = "../../assets/be27aa7e15ec11e0aa658ff1b7b1129385772382eef1b4c84542710d189cda78.svg";
const imgIcon3 = "../../assets/5617a341b13fade245cdbd3ee05fc8ba63cc1c642a5584f8c403c14c5b6cc83a.svg";
const imgIcon4 = "../../assets/be27aa7e15ec11e0aa658ff1b7b1129385772382eef1b4c84542710d189cda78.svg";
const imgIcon5 = "../../assets/be27aa7e15ec11e0aa658ff1b7b1129385772382eef1b4c84542710d189cda78.svg";

type RoundedBadgeProps = {
  className?: string;
  showIcon?: boolean;
  variation?: "Purple" | "Primary" | "Secondary" | "Overlay";
};

function RoundedBadge({ className, showIcon = true, variation = "Purple" }: RoundedBadgeProps) {
  const isOverlay = variation === "Overlay";
  const isPrimary = variation === "Primary";
  const isPurpleOrOverlay = ["Purple", "Overlay"].includes(variation);
  const isSecondary = variation === "Secondary";
  return (
    <div className={className || `${String.raw`content-stretch flex gap-[var(--$1,4px)] items-center px-[var(--$2,8px)] py-[var(--$1,4px)] relative rounded-[var(--radius\/5,40px)] `}${isOverlay ? String.raw`bg-[var(--background\/dim\/64,rgba(0,0,0,0.64))]` : isSecondary ? String.raw`bg-[var(--secondary\/default,#444954)]` : isPrimary ? String.raw`bg-[var(--primary\/default,#2572ed)]` : "bg-[#7e47eb]"}`} id={isOverlay ? "node-6012_270508" : isSecondary ? "node-6012_270505" : isPrimary ? "node-6012_270502" : "node-6012_270499"}>
      {isPurpleOrOverlay && showIcon && (
        <div className="relative shrink-0 size-[16px]" data-node-id="6012:270500" data-name="Icon">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon} />
        </div>
      )}
      {isPurpleOrOverlay && (
        <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[16px] not-italic relative shrink-0 text-[12px] text-[color:var(--on-surface\/high,#eff0fa)] tracking-[0.4px] whitespace-nowrap" id={isOverlay ? "node-6012_270510" : "node-6012_270501"}>
          Moderator
        </p>
      )}
      {isPrimary && showIcon && (
        <div className="relative shrink-0 size-[16px]" data-node-id="6012:270503" data-name="Icon">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon1} />
        </div>
      )}
      {isPrimary && (
        <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[16px] not-italic relative shrink-0 text-[12px] text-[color:var(--on-primary\/high,white)] tracking-[0.4px] whitespace-nowrap" data-node-id="6012:270504">
          Moderator
        </p>
      )}
      {isSecondary && showIcon && (
        <div className="relative shrink-0 size-[16px]" data-node-id="6012:270506" data-name="Icon">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon2} />
        </div>
      )}
      {isSecondary && (
        <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[16px] not-italic relative shrink-0 text-[12px] text-[color:var(--on-secondary\/high,white)] tracking-[0.4px] whitespace-nowrap" data-node-id="6012:270507">
          Moderator
        </p>
      )}
    </div>
  );
}

type BadgeProps = {
  className?: string;
  icon?: React.ReactNode | null;
  showIcon?: boolean;
  text?: string;
  variation?: "Primary" | "Purple" | "Secondary" | "Overlay";
};

function Badge({ className, icon = null, showIcon = true, text = "Moderator", variation = "Purple" }: BadgeProps) {
  const isOverlay = variation === "Overlay";
  const isPrimary = variation === "Primary";
  const isPurpleOrOverlay = ["Purple", "Overlay"].includes(variation);
  const isSecondary = variation === "Secondary";
  return (
    <div className={className || `${String.raw`content-stretch flex gap-[var(--$1,4px)] items-center px-[var(--$2,8px)] py-[var(--$1,4px)] relative rounded-[var(--radius\/0,4px)] `}${isOverlay ? String.raw`bg-[var(--background\/dim\/64,rgba(0,0,0,0.64))]` : isSecondary ? String.raw`bg-[var(--secondary\/default,#444954)]` : isPrimary ? String.raw`bg-[var(--primary\/default,#2572ed)]` : "bg-[#7e47eb]"}`} id={isOverlay ? "node-6012_270495" : isSecondary ? "node-6012_270492" : isPrimary ? "node-6012_270489" : "node-6012_270486"}>
      {isPurpleOrOverlay &&
        showIcon &&
        (icon || (
          <div className="relative shrink-0 size-[16px]" data-node-id="6012:270487" data-name="Icon">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon3} />
          </div>
        ))}
      {isPurpleOrOverlay && (
        <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[16px] not-italic relative shrink-0 text-[10px] text-[color:var(--on-surface\/high,#eff0fa)] tracking-[1.5px] uppercase whitespace-nowrap" data-node-id="6012:270488">
          {text}
        </p>
      )}
      {isPrimary &&
        showIcon &&
        (icon || (
          <div className="relative shrink-0 size-[16px]" data-node-id="6012:270490" data-name="Icon">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon4} />
          </div>
        ))}
      {isPrimary && (
        <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[16px] not-italic relative shrink-0 text-[10px] text-[color:var(--on-surface\/high,#eff0fa)] tracking-[1.5px] uppercase whitespace-nowrap" data-node-id="6012:270491">
          {text}
        </p>
      )}
      {isSecondary &&
        showIcon &&
        (icon || (
          <div className="relative shrink-0 size-[16px]" data-node-id="6012:270493" data-name="Icon">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIcon5} />
          </div>
        ))}
      {isSecondary && (
        <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[16px] not-italic relative shrink-0 text-[10px] text-[color:var(--on-surface\/high,#eff0fa)] tracking-[1.5px] uppercase whitespace-nowrap" data-node-id="6012:270494">
          {text}
        </p>
      )}
    </div>
  );
}

export default function Badge1() {
  return (
    <div className="content-stretch flex flex-col items-start relative size-full" data-node-id="6040:2348331" data-name="Badge">
      <div className="bg-[#131313] border-b-4 border-black border-solid content-stretch flex flex-col gap-[16px] items-start p-[64px] relative shrink-0 w-full" data-node-id="6012:270484" data-name="Figma File Header">
        <div className="[word-break:break-word] flex flex-col font-['Inter:Semi_Bold'] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[20px] text-[rgba(255,255,255,0.6)] tracking-[1.6px] uppercase whitespace-nowrap" data-node-id="I6012:270484;4703:103125">
          <p className="leading-[1.2]">Component</p>
        </div>
        <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-node-id="I6012:270484;4703:103126" data-name="Heading and supporting text">
          <div className="content-stretch flex gap-[24px] items-center relative shrink-0 w-full" data-node-id="I6012:270484;4703:103127" data-name="Heading">
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[72px] not-italic relative shrink-0 text-[56px] text-[rgba(255,255,255,0.9)] tracking-[-1.12px] whitespace-nowrap" data-node-id="I6012:270484;4703:103128">
              Badge
            </p>
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.2] not-italic relative shrink-0 text-[20px] text-[rgba(255,255,255,0.4)] w-full" data-node-id="I6012:270484;4703:103131">
            Use badge to label, categorize, or organize items using keywords that describe them.
          </p>
        </div>
      </div>
      <div className="bg-[#131313] h-[416px] relative shrink-0 w-[479px]" data-node-id="6040:2348330" />
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

These styles are contained in the design: Desktop/Overline-Medium-10px: Font(family: "Inter", style: Semi Bold, size: 10, weight: 600, lineHeight: 16, letterSpacing: 1.5), Desktop/Caption-Semibold-12px: Font(family: "Inter", style: Semi Bold, size: 12, weight: 600, lineHeight: 16, letterSpacing: 0.4000000059604645).

Images and SVGs will be stored as constants, e.g. const image = `${assetPathPrefix}/<asset file name>`, where assetPathPrefix is declared once at the top of the code and every asset URL interpolates it. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.
