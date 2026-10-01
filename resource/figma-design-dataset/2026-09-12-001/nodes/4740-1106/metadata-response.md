<frame id="4740:1106" name="107.1 Add Transactions " x="17245" y="-512" width="1440" height="1024">
  <rounded-rectangle id="4740:1107" name="107" x="0" y="0" width="1440" height="1024" />
  <frame id="4749:903" name="Add Transaction Button" x="1196" y="140" width="173" height="46">
    <text id="4749:904" name="+" x="20" y="12" width="13" height="22" />
    <text id="4749:905" name="Add Transaction" x="41" y="14.5" width="112" height="17" />
  </frame>
  <frame id="4749:906" name="Add Transaction Form" x="304" y="208" width="1104" height="704">
    <text id="4749:907" name="Add Transaction" x="32" y="28" width="191" height="29" />
    <text id="4749:908" name="Enter the transaction details below. Fields marked * are required." x="32" y="77" width="428" height="17" />
    <frame id="4749:1079" name="Form Row 1" x="32" y="114" width="1040" height="76">
      <frame id="4749:1080" name="Transaction Type Field" x="0" y="0" width="508" height="76">
        <text id="4749:1081" name="Transaction Type *" x="0" y="0" width="129" height="17" />
        <frame id="4749:1082" name="Transaction Type Field Control" x="0" y="25" width="508" height="48">
          <text id="4749:1083" name="Expense" x="16" y="13" width="57" height="17" />
        </frame>
      </frame>
      <frame id="4749:1084" name="Account Field" x="532" y="0" width="508" height="76">
        <text id="4749:1085" name="Account *" x="0" y="0" width="69" height="17" />
        <frame id="4749:1086" name="Account Field Control" x="0" y="25" width="508" height="48">
          <text id="4749:1087" name="Select account" x="16" y="13" width="99" height="17" />
        </frame>
      </frame>
    </frame>
    <frame id="4749:1088" name="Form Row 2" x="32" y="210" width="1040" height="76">
      <frame id="4749:1089" name="Amount Field" x="0" y="0" width="508" height="76">
        <text id="4749:1090" name="Amount *" x="0" y="0" width="65" height="17" />
        <frame id="4749:1091" name="Amount Field Control" x="0" y="25" width="508" height="48">
          <text id="4749:1092" name="0.00" x="16" y="13" width="30" height="17" />
        </frame>
      </frame>
      <frame id="4749:1093" name="Transaction Date Field" x="532" y="0" width="508" height="76">
        <text id="4749:1094" name="Transaction Date *" x="0" y="0" width="127" height="17" />
        <frame id="4749:1095" name="Transaction Date Field Control" x="0" y="25" width="508" height="48">
          <text id="4749:1096" name="13 Aug 2026" x="16" y="13" width="84" height="17" />
        </frame>
      </frame>
    </frame>
    <frame id="4749:1097" name="Form Row 3" x="32" y="306" width="1040" height="76">
      <frame id="4749:1098" name="Item Description Field" x="0" y="0" width="508" height="76">
        <text id="4749:1099" name="Item Description *" x="0" y="0" width="123" height="17" />
        <frame id="4749:1100" name="Item Description Field Control" x="0" y="25" width="508" height="48">
          <text id="4749:1101" name="Enter transaction description" x="16" y="13" width="192" height="17" />
        </frame>
      </frame>
      <frame id="4749:1102" name="Shop Name Field" x="532" y="0" width="508" height="76">
        <text id="4749:1103" name="Shop Name *" x="0" y="0" width="89" height="17" />
        <frame id="4749:1104" name="Shop Name Field Control" x="0" y="25" width="508" height="48">
          <text id="4749:1105" name="Enter shop or recipient name" x="16" y="13" width="191" height="17" />
        </frame>
      </frame>
    </frame>
    <frame id="4749:1106" name="Form Row 4" x="32" y="402" width="1040" height="76">
      <frame id="4749:1107" name="Payment Method Field" x="0" y="0" width="508" height="76">
        <text id="4749:1108" name="Payment Method *" x="0" y="0" width="127" height="17" />
        <frame id="4749:1109" name="Payment Method Field Control" x="0" y="25" width="508" height="48">
          <text id="4749:1110" name="Enter payment method" x="16" y="13" width="152" height="17" />
        </frame>
      </frame>
      <frame id="4749:1111" name="Category Field" x="532" y="0" width="508" height="76">
        <text id="4749:1112" name="Category (Optional)" x="0" y="0" width="135" height="17" />
        <frame id="4749:1113" name="Category Field Control" x="0" y="25" width="508" height="48">
          <text id="4749:1114" name="Select category" x="16" y="13" width="105" height="17" />
        </frame>
      </frame>
    </frame>
    <frame id="4749:1115" name="Form Actions" x="32" y="498" width="1040" height="48">
      <frame id="4749:1116" name="Cancel Button" x="767" y="1.5" width="96" height="45">
        <text id="4749:1117" name="Cancel" x="24" y="14" width="48" height="17" />
      </frame>
      <frame id="4749:1118" name="Save Transaction Button" x="875" y="1.5" width="165" height="45">
        <text id="4749:1119" name="Save Transaction" x="24" y="14" width="117" height="17" />
      </frame>
    </frame>
  </frame>
</frame>

IMPORTANT: After you call this tool, you MUST call get_design_context if trying to implement the design, since this tool only returns metadata. If you do not call get_design_context, the agent will not be able to implement the design.
