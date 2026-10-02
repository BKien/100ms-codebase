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

export default function Typography() {
  return (
    <div className="bg-white content-stretch flex flex-col items-start relative size-full" data-node-id="4707:66543" data-name="Typography">
      <FigmaFileHeader className="bg-[#131313] border-b-4 border-black border-solid content-stretch flex flex-col gap-[16px] items-start p-[64px] relative shrink-0 w-full" description="Use typography to present your design and content as clearly and efficiently as possible" title="Typography" />
      <div className="bg-[#131313] content-stretch flex flex-col gap-[96px] items-start px-[64px] py-[80px] relative shrink-0" data-node-id="4707:66545" data-name="Content">
        <div className="[word-break:break-word] content-stretch flex flex-col font-['Inter:Regular'] font-normal gap-[64px] items-start not-italic relative shrink-0 text-white w-full" data-node-id="4707:66546" data-name="Typeface">
          <div className="content-stretch flex flex-col gap-[16px] items-start leading-[normal] relative shrink-0 w-full whitespace-nowrap" data-node-id="4707:66547" data-name="Text">
            <p className="relative shrink-0 text-[48px]" data-node-id="4707:66548">
              Inter
            </p>
            <p className="relative shrink-0 text-[112px]" data-node-id="4707:66549">
              Ag
            </p>
          </div>
          <p className="leading-[60px] relative shrink-0 text-[48px] tracking-[-0.96px] w-full" data-node-id="4707:66550">
            ABCDEFGHIJKLMNOPQRSTUVWXYZ
            <br aria-hidden />
            abcdefghijklmnopqrstuvwxyz
            <br aria-hidden />
            {`0123456789 !@#$%^&*()`}
          </p>
        </div>
        <div className="content-stretch flex gap-[240px] items-start relative shrink-0" data-node-id="4995:36904" data-name="Unit">
          <div className="content-stretch flex flex-col gap-[32px] items-start relative shrink-0" data-node-id="4713:156984" data-name="Desktop">
            <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[48px] text-white whitespace-nowrap" data-node-id="4713:156985" style={{ fontVariationSettings: '"wdth" 100' }}>
              Desktop
            </p>
            <div className="content-stretch flex flex-col gap-[80px] items-start relative shrink-0" data-node-id="4713:156986" data-name="Section">
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59056" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59057" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Heading 1-Semibold-80px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59058" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59059" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59060" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59061" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59062" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59063" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59064" style={{ fontVariationSettings: '"wdth" 100' }}>
                        80px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59065" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59066" style={{ fontVariationSettings: '"wdth" 100' }}>
                        84px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59067" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[84px] not-italic relative shrink-0 text-[80px] text-white tracking-[-1.5px] whitespace-nowrap" data-node-id="5245:59068">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58972" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58973" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Heading 2-Semibold-60px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58974" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58975" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58976" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58977" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58978" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58979" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58980" style={{ fontVariationSettings: '"wdth" 100' }}>
                        60px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58981" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58982" style={{ fontVariationSettings: '"wdth" 100' }}>
                        60px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58983" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[60px] not-italic relative shrink-0 text-[60px] text-white tracking-[-0.5px] whitespace-nowrap" data-node-id="5245:58984">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59084" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59085" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Heading 3-Semibold-48px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59086" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59087" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59088" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59089" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59090" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59091" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59092" style={{ fontVariationSettings: '"wdth" 100' }}>
                        48px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59093" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59094" style={{ fontVariationSettings: '"wdth" 100' }}>
                        52px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59095" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[52px] not-italic relative shrink-0 text-[48px] text-white whitespace-nowrap" data-node-id="5245:59096">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59070" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59071" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Heading 4-Semibold-34px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59072" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59073" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59074" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59075" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59076" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59077" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59078" style={{ fontVariationSettings: '"wdth" 100' }}>
                        34px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59079" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59080" style={{ fontVariationSettings: '"wdth" 100' }}>
                        40px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59081" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[40px] not-italic relative shrink-0 text-[34px] text-white tracking-[0.25px] whitespace-nowrap" data-node-id="5245:59082">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59028" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59029" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Heading 5-Semibold-24px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59030" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59031" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59032" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59033" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59034" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59035" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59036" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59037" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59038" style={{ fontVariationSettings: '"wdth" 100' }}>
                        32px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59039" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[32px] not-italic relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59040">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59000" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59001" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Heading 6-Semibold-20px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59002" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59003" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59004" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59005" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59006" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59007" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59008" style={{ fontVariationSettings: '"wdth" 100' }}>
                        20px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59009" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59010" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59011" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[20px] text-white tracking-[0.15px] whitespace-nowrap" data-node-id="5245:59012">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58958" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58959" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Subtitle 1-Semibold-16px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58960" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58961" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58962" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58963" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58964" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58965" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58966" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58967" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58968" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58969" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-white tracking-[0.15px] whitespace-nowrap" data-node-id="5245:58970">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58930" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58931" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Subtitle 2-Semibold-14px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58932" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58933" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58934" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58935" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58936" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58937" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58938" style={{ fontVariationSettings: '"wdth" 100' }}>
                        14px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58939" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58940" style={{ fontVariationSettings: '"wdth" 100' }}>
                        20px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58941" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[20px] not-italic relative shrink-0 text-[14px] text-white tracking-[0.1px] whitespace-nowrap" data-node-id="5245:58942">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59042" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59043" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Button-Semibold-16px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59044" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59045" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59046" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59047" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59048" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59049" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59050" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59051" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59052" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59053" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-white tracking-[0.5px] whitespace-nowrap" data-node-id="5245:59054">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59014" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59015" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Body 1-Regular-16px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59016" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59017" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59018" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59019" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59020" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Regular
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59021" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59022" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59023" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59024" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59025" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[16px] text-white tracking-[0.5px] whitespace-nowrap" data-node-id="5245:59026">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58986" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58987" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Body 1-Semibold-16px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58988" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58989" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58990" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58991" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58992" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58993" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58994" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58995" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58996" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58997" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-white tracking-[0.5px] whitespace-nowrap" data-node-id="5245:58998">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58944" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58945" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Body 2-Regular-14px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58946" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58947" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58948" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58949" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58950" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Regular
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58951" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58952" style={{ fontVariationSettings: '"wdth" 100' }}>
                        14px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58953" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58954" style={{ fontVariationSettings: '"wdth" 100' }}>
                        20px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58955" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[14px] text-white tracking-[0.25px] whitespace-nowrap" data-node-id="5245:58956">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58916" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58917" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Body 2-Semibold-14px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58918" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58919" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58920" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58921" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58922" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58923" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58924" style={{ fontVariationSettings: '"wdth" 100' }}>
                        14px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58925" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58926" style={{ fontVariationSettings: '"wdth" 100' }}>
                        20px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58927" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[20px] not-italic relative shrink-0 text-[14px] text-white tracking-[0.25px] whitespace-nowrap" data-node-id="5245:58928">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58902" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58903" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Link-Semibold-14px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58904" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58905" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58906" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58907" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58908" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58909" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58910" style={{ fontVariationSettings: '"wdth" 100' }}>
                        14px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58911" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58912" style={{ fontVariationSettings: '"wdth" 100' }}>
                        20px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58913" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[20px] not-italic relative shrink-0 text-[14px] text-white tracking-[0.25px] whitespace-nowrap" data-node-id="5245:58914">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58888" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58889" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Caption-Regular-12px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58890" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58891" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58892" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58893" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58894" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Regular
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58895" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58896" style={{ fontVariationSettings: '"wdth" 100' }}>
                        12px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58897" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58898" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58899" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[16px] not-italic relative shrink-0 text-[12px] text-white tracking-[0.4px] whitespace-nowrap" data-node-id="5245:58900">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58874" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58875" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Caption-Semibold-12px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58876" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58877" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58878" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58879" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58880" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semibold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58881" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58882" style={{ fontVariationSettings: '"wdth" 100' }}>
                        12px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58883" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58884" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58885" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[16px] not-italic relative shrink-0 text-[12px] text-white tracking-[0.4px] whitespace-nowrap" data-node-id="5245:58886">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58860" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58861" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Overline-Medium-10px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58862" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58863" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58864" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58865" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58866" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58867" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58868" style={{ fontVariationSettings: '"wdth" 100' }}>
                        10px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58869" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58870" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58871" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[16px] not-italic relative shrink-0 text-[10px] text-white tracking-[1.5px] uppercase whitespace-nowrap" data-node-id="5245:58872">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:58846" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:58847" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Paragraph-18px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:58848" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:58849" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58850" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:58851" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58852" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Regular
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:58853" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:58854" style={{ fontVariationSettings: '"wdth" 100' }}>
                        18px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58855" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:58856" style={{ fontVariationSettings: '"wdth" 100' }}>
                        36px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:58857" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[36px] not-italic relative shrink-0 text-[18px] text-white tracking-[0.5px] whitespace-nowrap" data-node-id="5245:58858">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="content-stretch flex flex-col gap-[32px] items-start relative shrink-0" data-node-id="4713:157239" data-name="Mobile">
            <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[48px] text-white whitespace-nowrap" data-node-id="4713:157240" style={{ fontVariationSettings: '"wdth" 100' }}>
              Mobile
            </p>
            <div className="content-stretch flex flex-col gap-[80px] items-start relative shrink-0" data-node-id="4713:157241" data-name="Section">
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59252" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59253" style={{ fontVariationSettings: '"wdth" 100' }}>
                  H1-Semibold-72px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59254" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59255" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59256" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59257" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59258" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59259" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59260" style={{ fontVariationSettings: '"wdth" 100' }}>
                        72px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59261" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59262" style={{ fontVariationSettings: '"wdth" 100' }}>
                        76px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59263" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[76px] not-italic relative shrink-0 text-[72px] text-white tracking-[-1.5px] whitespace-nowrap" data-node-id="5245:59264">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59210" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59211" style={{ fontVariationSettings: '"wdth" 100' }}>
                  H2-Semibold-48px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59212" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59213" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59214" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59215" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59216" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59217" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59218" style={{ fontVariationSettings: '"wdth" 100' }}>
                        48px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59219" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59220" style={{ fontVariationSettings: '"wdth" 100' }}>
                        52px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59221" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[52px] not-italic relative shrink-0 text-[48px] text-white tracking-[-0.5px] whitespace-nowrap" data-node-id="5245:59222">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59196" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59197" style={{ fontVariationSettings: '"wdth" 100' }}>
                  H3-Semibold-40px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59198" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59199" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59200" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59201" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59202" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59203" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59204" style={{ fontVariationSettings: '"wdth" 100' }}>
                        40px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59205" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59206" style={{ fontVariationSettings: '"wdth" 100' }}>
                        44px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59207" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[44px] not-italic relative shrink-0 text-[40px] text-white whitespace-nowrap" data-node-id="5245:59208">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59182" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59183" style={{ fontVariationSettings: '"wdth" 100' }}>
                  H4-Semibold-28px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59184" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59185" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59186" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59187" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59188" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59189" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59190" style={{ fontVariationSettings: '"wdth" 100' }}>
                        28px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59191" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59192" style={{ fontVariationSettings: '"wdth" 100' }}>
                        32px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59193" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[32px] not-italic relative shrink-0 text-[28px] text-white tracking-[0.25px] whitespace-nowrap" data-node-id="5245:59194">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59168" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59169" style={{ fontVariationSettings: '"wdth" 100' }}>
                  H5-Semibold-24px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59170" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59171" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59172" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59173" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59174" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59175" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59176" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59177" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59178" style={{ fontVariationSettings: '"wdth" 100' }}>
                        28px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59179" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[28px] not-italic relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59180">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59154" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59155" style={{ fontVariationSettings: '"wdth" 100' }}>
                  H6-Semibold-20px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59156" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59157" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59158" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59159" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59160" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59161" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59162" style={{ fontVariationSettings: '"wdth" 100' }}>
                        20px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59163" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59164" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59165" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[20px] text-white tracking-[0.15px] whitespace-nowrap" data-node-id="5245:59166">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59140" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59141" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Subtitle 1-Medium-16px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59142" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59143" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59144" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59145" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59146" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Medium
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59147" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59148" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59149" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59150" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59151" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[24px] not-italic relative shrink-0 text-[16px] text-white tracking-[0.15px] whitespace-nowrap" data-node-id="5245:59152">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59126" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59127" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Subtitle 2-Medium-14px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59128" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59129" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59130" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59131" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59132" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Medium
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59133" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59134" style={{ fontVariationSettings: '"wdth" 100' }}>
                        14px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59135" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59136" style={{ fontVariationSettings: '"wdth" 100' }}>
                        20px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59137" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[20px] not-italic relative shrink-0 text-[14px] text-white tracking-[0.1px] whitespace-nowrap" data-node-id="5245:59138">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59112" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59113" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Body 1-Regular-16px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59114" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59115" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59116" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59117" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59118" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Regular
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59119" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59120" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59121" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59122" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59123" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[24px] not-italic relative shrink-0 text-[16px] text-white tracking-[0.5px] whitespace-nowrap" data-node-id="5245:59124">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59238" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59239" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Body 2-Regular-14px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59240" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59241" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59242" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59243" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59244" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Regular
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59245" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59246" style={{ fontVariationSettings: '"wdth" 100' }}>
                        14px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59247" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59248" style={{ fontVariationSettings: '"wdth" 100' }}>
                        20px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59249" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[20px] not-italic relative shrink-0 text-[14px] text-white tracking-[0.25px] whitespace-nowrap" data-node-id="5245:59250">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59224" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59225" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Button-Semibold-16px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59226" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59227" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59228" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59229" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59230" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59231" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59232" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59233" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59234" style={{ fontVariationSettings: '"wdth" 100' }}>
                        24px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59235" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[24px] not-italic relative shrink-0 text-[16px] text-white tracking-[0.5px] whitespace-nowrap" data-node-id="5245:59236">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59098" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59099" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Caption-Regular-12px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59100" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59101" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59102" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59103" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59104" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Regular
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59105" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59106" style={{ fontVariationSettings: '"wdth" 100' }}>
                        12px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59107" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59108" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59109" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[16px] not-italic relative shrink-0 text-[12px] text-white tracking-[0.4px] whitespace-nowrap" data-node-id="5245:59110">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-node-id="5245:59266" data-name="Text component">
                <p className="[word-break:break-word] font-['Roboto:Bold'] font-bold leading-[normal] relative shrink-0 text-[24px] text-white whitespace-nowrap" data-node-id="5245:59267" style={{ fontVariationSettings: '"wdth" 100' }}>
                  Overline-Medium-10px
                </p>
                <div className="content-stretch flex gap-[8px] items-start relative shrink-0" data-node-id="5245:59268" data-name="Body">
                  <div className="[word-break:break-word] content-stretch flex flex-col font-['Roboto:Regular'] font-normal gap-[8px] items-start leading-[normal] relative shrink-0 text-[14px] text-white w-[200px] whitespace-nowrap" data-node-id="5245:59269" data-name="Spec">
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59270" data-name="FontName">
                      <p className="relative shrink-0" data-node-id="5245:59271" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Inter
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59272" style={{ fontVariationSettings: '"wdth" 100' }}>
                        Semi Bold
                      </p>
                    </div>
                    <div className="content-stretch flex gap-[4px] items-start relative shrink-0" data-node-id="5245:59273" data-name="FontSize">
                      <p className="relative shrink-0" data-node-id="5245:59274" style={{ fontVariationSettings: '"wdth" 100' }}>
                        10px
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59275" style={{ fontVariationSettings: '"wdth" 100' }}>
                        /
                      </p>
                      <p className="relative shrink-0" data-node-id="5245:59276" style={{ fontVariationSettings: '"wdth" 100' }}>
                        16px
                      </p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0" data-node-id="5245:59277" data-name="Guide">
                    <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[16px] not-italic relative shrink-0 text-[10px] text-white tracking-[1.5px] uppercase whitespace-nowrap" data-node-id="5245:59278">
                      The quick brown fox jumps over the lazy dog.
                    </p>
                  </div>
                </div>
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

These styles are contained in the design: Display lg/Normal: Font(family: "Inter", style: Regular, size: 48, weight: 400, lineHeight: 60, letterSpacing: -2), Desktop/Heading 1-Semibold-80px: Font(family: "Inter", style: Semi Bold, size: 80, weight: 600, lineHeight: 84, letterSpacing: -1.5), Desktop/Heading 2-Semibold-60px: Font(family: "Inter", style: Semi Bold, size: 60, weight: 600, lineHeight: 60, letterSpacing: -0.5), Desktop/Heading 3-Semibold-48px: Font(family: "Inter", style: Semi Bold, size: 48, weight: 600, lineHeight: 52, letterSpacing: 0), Desktop/Heading 4-Semibold-34px: Font(family: "Inter", style: Semi Bold, size: 34, weight: 600, lineHeight: 40, letterSpacing: 0.25), Desktop/Heading 5-Semibold-24px: Font(family: "Inter", style: Semi Bold, size: 24, weight: 600, lineHeight: 32, letterSpacing: 0), Desktop/Heading 6-Semibold-20px: Font(family: "Inter", style: Semi Bold, size: 20, weight: 600, lineHeight: 24, letterSpacing: 0.15000000596046448), Desktop/Subtitle 1-Semibold-16px: Font(family: "Inter", style: Semi Bold, size: 16, weight: 600, lineHeight: 24, letterSpacing: 0.15000000596046448), Desktop/Subtitle 2-Semibold-14px: Font(family: "Inter", style: Semi Bold, size: 14, weight: 600, lineHeight: 20, letterSpacing: 0.10000000149011612), Desktop/Button-Semibold-16px: Font(family: "Inter", style: Semi Bold, size: 16, weight: 600, lineHeight: 24, letterSpacing: 0.5), Desktop/Body 1-Regular-16px: Font(family: "Inter", style: Regular, size: 16, weight: 400, lineHeight: 24, letterSpacing: 0.5), Desktop/Body 1-Semibold-16px: Font(family: "Inter", style: Semi Bold, size: 16, weight: 600, lineHeight: 24, letterSpacing: 0.5), Desktop/Body 2-Regular-14px: Font(family: "Inter", style: Regular, size: 14, weight: 400, lineHeight: 20, letterSpacing: 0.25), Desktop/Body 2-Semibold-14px: Font(family: "Inter", style: Semi Bold, size: 14, weight: 600, lineHeight: 20, letterSpacing: 0.25), Desktop/Link-Semibold-14px: Font(family: "Inter", style: Semi Bold, size: 14, weight: 600, lineHeight: 20, letterSpacing: 0.25), Desktop/Caption-Regular-12px: Font(family: "Inter", style: Regular, size: 12, weight: 400, lineHeight: 16, letterSpacing: 0.4000000059604645), Desktop/Caption-Semibold-12px: Font(family: "Inter", style: Semi Bold, size: 12, weight: 600, lineHeight: 16, letterSpacing: 0.4000000059604645), Desktop/Overline-Medium-10px: Font(family: "Inter", style: Semi Bold, size: 10, weight: 600, lineHeight: 16, letterSpacing: 1.5), Desktop/Paragraph-18px: Font(family: "Inter", style: Regular, size: 18, weight: 400, lineHeight: 36, letterSpacing: 0.5), Mobile/H1-Semibold-72px: Font(family: "Inter", style: Semi Bold, size: 72, weight: 600, lineHeight: 76, letterSpacing: -1.5), Mobile/H2-Semibold-48px: Font(family: "Inter", style: Semi Bold, size: 48, weight: 600, lineHeight: 52, letterSpacing: -0.5), Mobile/H3-Semibold-40px: Font(family: "Inter", style: Semi Bold, size: 40, weight: 600, lineHeight: 44, letterSpacing: 0), Mobile/H4-Semibold-28px: Font(family: "Inter", style: Semi Bold, size: 28, weight: 600, lineHeight: 32, letterSpacing: 0.25), Mobile/H5-Semibold-24px: Font(family: "Inter", style: Semi Bold, size: 24, weight: 600, lineHeight: 28, letterSpacing: 0), Mobile/H6-Semibold-20px: Font(family: "Inter", style: Semi Bold, size: 20, weight: 600, lineHeight: 24, letterSpacing: 0.15000000596046448), Mobile/Subtitle 1-Medium-16px: Font(family: "Inter", style: Medium, size: 16, weight: 500, lineHeight: 24, letterSpacing: 0.15000000596046448), Mobile/Subtitle 2-Medium-14px: Font(family: "Inter", style: Medium, size: 14, weight: 500, lineHeight: 20, letterSpacing: 0.10000000149011612), Mobile/Body 1-Regular-16px: Font(family: "Inter", style: Regular, size: 16, weight: 400, lineHeight: 24, letterSpacing: 0.5), Mobile/Body 2-Regular-14px: Font(family: "Inter", style: Regular, size: 14, weight: 400, lineHeight: 20, letterSpacing: 0.25), Mobile/Button-Semibold-16px: Font(family: "Inter", style: Semi Bold, size: 16, weight: 600, lineHeight: 24, letterSpacing: 0.5), Mobile/Caption-Regular-12px: Font(family: "Inter", style: Regular, size: 12, weight: 400, lineHeight: 16, letterSpacing: 0.4000000059604645), Mobile/Overline-Medium-10px: Font(family: "Inter", style: Semi Bold, size: 10, weight: 600, lineHeight: 16, letterSpacing: 1.5).

Images and SVGs will be stored as constants, e.g. const image = `${assetPathPrefix}/<asset file name>`, where assetPathPrefix is declared once at the top of the code and every asset URL interpolates it. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.
