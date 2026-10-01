# Tailwind CSS 3 and Recharts rules

## Tailwind

- Use existing Tailwind theme tokens/utilities and component patterns; avoid inline styles and duplicated arbitrary values.
- Work mobile-first: unprefixed utilities define the base layout; breakpoint variants enhance larger viewports.
- Keep conditional class construction readable and deterministic. Do not generate class names dynamically in ways Tailwind cannot detect.
- Maintain visible focus, readable contrast, text wrapping and overflow behavior at supported sizes.

## Recharts

- Keep chart data typed and transform it outside JSX. Use stable `dataKey` values matching the typed view model.
- Wrap responsive charts in `ResponsiveContainer` whose parent has a defined usable size.
- Provide axis/legend/unit labels and safe tooltip formatters. Do not expose raw sensitive data in tooltips.
- Preserve the accessibility layer and provide a text summary/table when the visualization alone cannot convey the result accessibly.
- Format numeric/date values consistently with project utilities; never rely on floating-point display defaults for precision-sensitive values.

Official basis:

- https://tailwindcss.com/docs/responsive-design
- https://recharts.github.io/en-US/api/ResponsiveContainer/
- https://recharts.github.io/en-US/api/PieChart/

