# Business Rule baseline

Before generation, freeze a receipt containing the UC path/checksum, Sheet provenance, ordered BR IDs and timestamp.

All Sheet-supplied BRs for the UC are included. This gate does not select or score rules; it prevents the evaluated rule set from changing after generation begins.

If the UC projection and Sheet differ, stop and ask the researcher before freezing. A documented source typo may be carried as an unresolved discrepancy without changing its business meaning.
