import { Link } from 'react-router-dom'

const section = 'mb-8'
const heading = 'text-xl font-bold text-gray-900 mb-3'
const sub = 'text-sm text-gray-600 leading-relaxed'
const list = 'list-disc list-inside text-sm text-gray-600 leading-relaxed space-y-1'

const PrivacyPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="card !p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Privacy Policy</h1>
            <p className="text-sm text-gray-500">
              Effective date: 7 August 2026 · Republic of Kenya · Kenya Data Protection Act, 2019
            </p>
            <p className="text-sm text-gray-600 mt-3 leading-relaxed">
              N.O.U. Digital Systems recognizes the importance of protecting personal information.
              This policy explains how we collect, use, store, protect, and disclose personal data in
              connection with our website, applications, services, assessments, customer
              relationships, and employment processes.
            </p>
          </div>

          <div className={section}>
            <h2 className={heading}>What we collect</h2>
            <p className={sub}>Depending on the service, N.O.U. may collect:</p>
            <ul className={list + ' mt-2'}>
              <li><strong>Account information:</strong> name, email, telephone, username, securely protected password credentials, account role, and account activity.</li>
              <li><strong>Customer information:</strong> project requirements, business information, communications, transaction information, service history, and support requests.</li>
              <li><strong>Applicant information:</strong> name, contact details, education, professional information, technical skills, assessment responses and results, CVs, and portfolios.</li>
              <li><strong>Technical information:</strong> IP address, browser type, operating system, device information, access times, security and error logs, and usage information.</li>
              <li><strong>Investor information:</strong> country, contact details, proposed contribution, investment expectations, and stated risk knowledge.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>Why we process it</h2>
            <ul className={list}>
              <li>Creating and managing accounts.</li>
              <li>Providing services, processing customer requests, and developing and delivering software.</li>
              <li>Administering assessments and recruitment.</li>
              <li>Customer support, authentication, security, and fraud prevention.</li>
              <li>System monitoring, billing, improving services, and communicating with users.</li>
              <li>Complying with legal obligations.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>Legal basis &amp; sharing</h2>
            <p className={sub}>
              We may process personal data based on consent, performance of a contract, compliance
              with a legal obligation, legitimate interests where permitted by law, or another lawful
              basis recognized under applicable law.
            </p>
            <ul className={list + ' mt-3'}>
              <li>N.O.U. does not sell personal data.</li>
              <li>Data may be shared where reasonably necessary with hosting, cloud, communication, payment, and security providers, professional advisers, authorized contractors, and regulatory or law-enforcement authorities where legally required.</li>
              <li>Some providers may process or store information outside Kenya; where data is transferred outside Kenya we take reasonable steps to comply with applicable Kenyan data-protection requirements.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>Retention &amp; security</h2>
            <ul className={list}>
              <li>Personal data is retained no longer than reasonably necessary for the purpose collected, unless a longer period is required or permitted by law.</li>
              <li>We apply reasonable technical and organizational safeguards: encrypted communications, password hashing, access controls, role-based permissions, authentication, logging, monitoring, backups, security testing, and incident-response procedures.</li>
              <li>No online system can be guaranteed completely secure.</li>
            </ul>
          </div>

          <div className={section}>
            <h2 className={heading}>Your rights</h2>
            <p className={sub}>
              Subject to applicable legal conditions, you may have rights to be informed, access,
              correct, object, delete or erase, restrict processing, data portability, and withdraw
              consent where processing is based on consent.
            </p>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-sm text-gray-600 mt-3 space-y-1">
              <p><strong>Privacy contact:</strong> <a href="mailto:nouprivacy@gmail.com" className="text-primary-600 hover:text-primary-700">nouprivacy@gmail.com</a></p>
              <p>Website: nou.com · Country: Kenya</p>
              <p>Where a matter cannot be resolved directly, you may exercise any right available under applicable Kenyan law, including lodging a complaint with the relevant regulatory authority (e.g. the Office of the Data Protection Commissioner, Kenya).</p>
            </div>
          </div>

          <div className={section}>
            <h2 className={heading}>First-login agreement</h2>
            <p className={sub}>
              On first login you must review and agree to these terms before you can submit personal
              details, participate in assessments, invest, join projects, or use other platform
              features. Your agreement is recorded with a timestamp on your account.
            </p>
          </div>

          <div className="mt-8 pt-6 border-t border-gray-200">
            <Link to="/terms" className="btn-secondary">Read the Terms &amp; Conditions</Link>
            <Link to="/" className="btn-outline ml-3">Back to home</Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PrivacyPage
