-- thm_mode = {
--     "thm",
--     "prop",
--     "defi",
--     "cor"
-- }

function Div (d)
    for i = 1, #thm_mode do
        if thm_mode[i] == d.attr.classes[1] then
            d.content[1].content[1].content[1] = pandoc.Para("")
            local result = d.content
            result:insert(1, pandoc.RawInline("typst", "#"..d.attr.classes[1].."["))
            result:insert(pandoc.RawInline("typst", "]"))
            return result
        end
    end
    return d
end

function Emph (e)
    return e.content
end
