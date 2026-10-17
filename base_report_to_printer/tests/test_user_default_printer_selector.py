# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import Form, common, new_test_user


class TestUserDefaultPrinterSelector(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.printer = cls.env["printing.printer"].create(
            {"name": "Warehouse printer", "system_name": "warehouse"}
        )
        cls.user = new_test_user(
            cls.env,
            login="printer_user",
            groups="base.group_user,base_report_to_printer.printer_button_group",
        )

    def test_select_printer_from_navbar(self):
        """The printer button of the navbar sets the default printer of the
        user"""
        action = self.env.ref(
            "base_report_to_printer.action_user_default_printer_selector"
        )
        wizard_model = self.env[action.res_model].with_user(self.user)
        with Form(wizard_model) as wizard_form:
            self.assertFalse(wizard_form.printing_printer_id)
            wizard_form.printing_printer_id = self.printer
        wizard_form.record.action_confirm()
        self.assertEqual(self.user.printing_printer_id, self.printer)
        # The wizard proposes the current printer of the user next time
        self.assertEqual(wizard_model.create({}).printing_printer_id, self.printer)
