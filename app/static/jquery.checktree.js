;
(function (win, doc, $) {
	$.fn.extend({
		checktree : function () {
			this.click(function (evt) {
				var evtEle = $(evt.target).closest("input:checkbox");
				if (!evtEle[0]) {
					return;
				}
				//check child all
				evtEle.parent().next(".checks").find("input:checkbox").attr("checked", evtEle[0].checked);

				//check parent
				if (evtEle.is("input:checked")) {
					evtEle.parents(".checks").each(function () {
						!$(this).children("p").children("input:checkbox").filter(function () {
							return !this.checked;
						})[0] && $(this).prev().children("input:checkbox").attr("checked", "checked");
					});
				} else {
					evtEle.parents(".checks").prev().children("input:checkbox").attr("checked", false);
				}
			});
		}
	});
})(window, document, jQuery);