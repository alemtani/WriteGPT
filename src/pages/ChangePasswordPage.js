import { useState, useEffect, useRef } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useNavigate } from 'react-router-dom';
import Body from '../components/Body';
import InputField from '../components/InputField';
import { useApi } from '../contexts/ApiProvider';
import { useFlash } from '../contexts/FlashProvider';
import { useUser } from '../contexts/UserProvider';

export default function ChangePasswordPage() {
    const [formErrors, setFormErrors] = useState({});
    const oldPasswordField = useRef();
    const passwordField = useRef();
    const password2Field = useRef();
    const navigate = useNavigate();
    const api = useApi();
    const flash = useFlash();
    const { user } = useUser();

    useEffect(() => {
        oldPasswordField.current.focus();
    }, []);

    const onSubmit = async (e) => {
        e.preventDefault();
        const old_password = oldPasswordField.current.value;
        const password = passwordField.current.value;
        const password2 = password2Field.current.value;

        const errors = {};
        if (!old_password) {
            errors.oldPassword = 'Old password must not be empty.';
        }
        if (!password) {
            errors.password = 'New password must not be empty.';
        }
        if (!password2) {
            errors.password2 = 'New password again must not be empty.';
        }
        if (password !== password2) {
            errors.password2 = "Passwords don't match.";
        }
        setFormErrors(errors);
        if (Object.keys(errors).length > 0) {
            return;
        }

        const response = await api.put(`/prompters/${user.id}`, {
            old_password,
            password
        });
        setFormErrors({});
        if (!response.ok) {
            flash(response.body.message, 'danger');
        } else {
            flash('You have successfully changed your password!', 'success');
            navigate(`/prompter/${user.id}`);
        }
    };

    return (
        <Body sidebar>
            <h1>Change Your Password</h1>
            <Form onSubmit={onSubmit}>
                <InputField
                    name="oldPassword" label="Old Password" type="password"
                    error={formErrors.oldPassword} fieldRef={oldPasswordField} />
                <InputField
                    name="password" label="New Password" type="password"
                    error={formErrors.password} fieldRef={passwordField} />
                <InputField
                    name="password2" label="New Password Again" type="password"
                    error={formErrors.password2} fieldRef={password2Field} />
                <Button variant="primary" type="submit">Change Password</Button>
            </Form>
        </Body>
    );
}