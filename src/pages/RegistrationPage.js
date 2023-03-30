import { useState, useEffect, useRef } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Body from '../components/Body';
import InputField from '../components/InputField';
import { Link, useNavigate } from 'react-router-dom';
import { useApi } from '../contexts/ApiProvider';
import { useFlash } from '../contexts/FlashProvider';

export default function RegistrationPage() {
    const [formErrors, setFormErrors] = useState({});
    const usernameField = useRef();
    const emailField = useRef();
    const passwordField = useRef();
    const password2Field = useRef();
    const navigate = useNavigate();
    const api = useApi();
    const flash = useFlash();

    useEffect(() => {
        usernameField.current.focus();
    }, []);

    const onSubmit = async (e) => {
        e.preventDefault();
        const username = usernameField.current.value;
        const email = emailField.current.value;
        const password = passwordField.current.value;
        const password2 = password2Field.current.value;

        const errors = {};
        if (!username) {
            errors.username = 'Username must not be empty.';
        }
        if (!email) {
            errors.email = 'Email address must not be empty.';
        }
        if (!password) {
            errors.password = 'Password must not be empty.';
        }
        if (!password2) {
            errors.password2 = 'Password again must not be empty.';
        }
        if (password !== password2) {
            errors.password2 = "Passwords don't match.";
        }
        setFormErrors(errors);
        if (Object.keys(errors).length > 0) {
            return;
        }

        const data = await api.post('/prompters', {
            username,
            email,
            password
        });
        setFormErrors({});
        if (!data.ok) {
            flash(data.body.message, 'danger');
        } else {
            flash('You have successfully registered!', 'success');
            navigate('/login');
        }
    };

    return (
        <Body>
            <h1>Register</h1>
            <Form onSubmit={onSubmit}>
                <InputField
                    name="username" label="Username"
                    error={formErrors.username} fieldRef={usernameField} />
                <InputField
                    name="email" label="Email address" type="email"
                    error={formErrors.email} fieldRef={emailField} />
                <InputField
                    name="password" label="Password" type="password"
                    error={formErrors.password} fieldRef={passwordField} />
                <InputField
                    name="password2" label="Password again" type="password"
                    error={formErrors.password2} fieldRef={password2Field} />
                <Button variant="primary" type="submit">Register</Button>
            </Form>
            <hr />
            <p>Already have an account? <Link to="/login">Login here</Link>!</p>
        </Body>
    );
}