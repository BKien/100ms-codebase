<frame id="66:5320" name="105. View Bank Accounts" x="1941" y="-512" width="1440" height="1024">
  <frame id="410:5547" name="Balances" x="304" y="104" width="1104" height="656">
    <text id="66:5347" name="Balances" x="0" y="0" width="94" height="32" />
    <frame id="410:5546" name="Account Type" x="0" y="48" width="1104" height="608">
      <frame id="410:5398" name="Top line" x="0" y="0" width="1104" height="288">
        <instance id="410:5376" name="Account Type" x="0" y="0" width="352" height="288" />
        <instance id="410:5354" name="Account Type" x="376" y="0" width="352" height="288" />
        <instance id="410:5421" name="Account Type" x="752" y="0" width="352" height="288" />
      </frame>
      <frame id="410:5515" name="Bottom Line" x="0" y="320" width="1104" height="288">
        <instance id="410:5492" name="Account Type" x="0" y="0" width="352" height="288" />
        <instance id="410:5469" name="Account Type" x="376" y="0" width="352" height="288" />
        <frame id="410:5516" name="Add Account" x="752" y="0" width="352" height="288">
          <frame id="410:5517" name="Button" x="72" y="100" width="208" height="100">
            <instance id="410:5539" name="Button Big" x="0" y="0" width="208" height="48" />
            <frame id="410:5545" name="Frame 133537" x="0" y="52" width="208" height="48">
              <text id="410:5530" name="Edit Accounts" x="24" y="12" width="160" height="24" />
            </frame>
          </frame>
        </frame>
      </frame>
    </frame>
  </frame>
  <instance id="411:6111" name="Header" x="280" y="0" width="1160" height="88" />
  <instance id="413:7727" name="Nav bar" x="0" y="0" width="280" height="1024" />
</frame>

IMPORTANT: After you call this tool, you MUST call get_design_context if trying to implement the design, since this tool only returns metadata. If you do not call get_design_context, the agent will not be able to implement the design.
