const assetPathPrefix = "../../assets";
const imgFigma = "assets-pending/72e4822601922ba6aebd22ddebab4920b4380458596d0481dd3db24b959587fd";

export default function Figma() {
  return (
    <div className="contents relative size-full" data-node-id="6062:48" data-name="Figma">
      <div className="absolute bg-[#0d0416] content-stretch flex flex-col gap-[48px] items-start left-0 overflow-clip p-[80px] rounded-[40px] top-0 w-[1342px]" data-node-id="6062:49" data-name="New?">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[16px] items-start not-italic relative shrink-0 w-[819px]" data-node-id="6062:50" data-name="Text">
          <p className="font-['Inter:Semi_Bold'] font-semibold leading-[1.2] relative shrink-0 text-[40px] text-[rgba(248,248,248,0.95)] w-full" data-node-id="6062:51">
            New to Figma?
          </p>
          <div className="font-['Inter:Regular'] font-normal leading-[0] relative shrink-0 text-[24px] text-[rgba(240,240,240,0.8)] w-full whitespace-pre-wrap" data-node-id="6062:52">
            <p className="leading-[1.6] mb-0">Our Kit makes use of the latest Figma features, including auto-layout, variables, components and variants.</p>
            <p className="leading-[1.6] mb-0">​</p>
            <p className="leading-[1.6]">{`If you're new to Figma, here are some resources from Figma themselves to get up and running as soon as possible:`}</p>
          </div>
        </div>
        <div className="[word-break:break-word] content-stretch flex flex-col font-['Inter:Semi_Bold'] font-semibold gap-[24px] items-start leading-[0] not-italic relative shrink-0 text-[#f0f0f0] text-[24px]" data-node-id="6062:53" data-name="Links">
          <p className="relative shrink-0 w-[819px]" data-node-id="6062:54">
            <span className="leading-[1.6]">{`-> `}</span>
            <a className="[text-decoration-skip-ink:none] [text-underline-position:from-font] cursor-pointer decoration-from-font decoration-solid leading-[1.6] underline" href="https://youtube.com/playlist?list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4" target="_blank">
              <span className="[text-decoration-skip-ink:none] [text-underline-position:from-font] decoration-from-font decoration-solid underline" href="https://youtube.com/playlist?list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4" target="_blank">
                Video Tutorials for Beginners
              </span>
            </a>
          </p>
          <p className="relative shrink-0 w-[819px]" data-node-id="6062:55">
            <span className="leading-[1.6]">{`-> `}</span>
            <a className="[text-decoration-skip-ink:none] [text-underline-position:from-font] cursor-pointer decoration-from-font decoration-solid leading-[1.6] underline" href="https://www.figma.com/best-practices/guides/" target="_blank">
              <span className="[text-decoration-skip-ink:none] [text-underline-position:from-font] decoration-from-font decoration-solid underline" href="https://www.figma.com/best-practices/guides/" target="_blank">
                Figma’s Best Practices Guides
              </span>
            </a>
          </p>
          <p className="relative shrink-0 w-[819px]" data-node-id="6062:56">
            <span className="leading-[1.6]">{`-> `}</span>
            <a className="[text-decoration-skip-ink:none] [text-underline-position:from-font] cursor-pointer decoration-from-font decoration-solid leading-[1.6] underline" href="https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-Components-in-Figma" target="_blank">
              <span className="[text-decoration-skip-ink:none] [text-underline-position:from-font] decoration-from-font decoration-solid underline" href="https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-Components-in-Figma" target="_blank">
                Guide to components in Figma
              </span>
            </a>
          </p>
          <p className="relative shrink-0 w-[819px]" data-node-id="6062:57">
            <span className="leading-[1.6]">{`-> `}</span>
            <a className="[text-decoration-skip-ink:none] [text-underline-position:from-font] cursor-pointer decoration-from-font decoration-solid leading-[1.6] underline" href="https://www.youtube.com/watch?v=1ONxxlJnvdM" target="_blank">
              <span className="[text-decoration-skip-ink:none] [text-underline-position:from-font] decoration-from-font decoration-solid underline" href="https://www.youtube.com/watch?v=1ONxxlJnvdM" target="_blank">
                Video: Introduction to Variables
              </span>
            </a>
          </p>
          <p className="relative shrink-0 w-[819px]" data-node-id="6062:58">
            <span className="leading-[1.6]">{`-> `}</span>
            <a className="[text-decoration-skip-ink:none] [text-underline-position:from-font] cursor-pointer decoration-from-font decoration-solid leading-[1.6] underline" href="https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma" target="_blank">
              <span className="[text-decoration-skip-ink:none] [text-underline-position:from-font] decoration-from-font decoration-solid underline" href="https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma" target="_blank">
                Guide to variables in Figma
              </span>
            </a>
          </p>
        </div>
        <div className="-translate-y-1/2 absolute h-[424px] right-[50px] top-1/2 w-[283px]" data-node-id="6062:59" data-name="Figma">
          <img alt="" className="absolute inset-0 max-w-none mix-blend-luminosity object-cover opacity-5 pointer-events-none size-full" src={imgFigma} />
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
