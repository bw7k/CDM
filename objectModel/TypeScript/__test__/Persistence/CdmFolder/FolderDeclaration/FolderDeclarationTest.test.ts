import { CdmManifestDeclarationDefinition } from '../../../../Cdm/CdmManifestDeclarationDefinition';
import { CdmManifestDefinition } from '../../../../Cdm/CdmManifestDefinition';
import { CdmCorpusDefinition } from '../../../../internal';
import { ManifestPersistence } from '../../../../Persistence/CdmFolder';
import { ManifestContent } from '../../../../Persistence/CdmFolder/types';
import { resolveContext } from '../../../../Utilities/resolveContext';
import { testHelper } from '../../../testHelper';

describe('Persistence.CdmFolder.FolderDeclaration', () => {
    /// <summary>
    /// The path between TestDataPath and TestName.
    /// </summary>
    const testsSubpath: string = 'Persistence/CdmFolder/FolderDeclaration';

    /**
     * Testing for folder impl instance with subfolders
     */
    it('TestLoadFolderWithSubFolders', () => {
        const content: string = testHelper.getInputFileContent(testsSubpath, 'TestLoadFolderWithSubFolders', 'subManifest.manifest.cdm.json');
        const context: resolveContext = new resolveContext(new CdmCorpusDefinition(), undefined);
        const cdmManifest: CdmManifestDefinition =
            ManifestPersistence.fromData(context, 'testEntity', 'testNamespace', '/', JSON.parse(content) as ManifestContent);
        expect(cdmManifest.subManifests.length)
            .toEqual(1);
        const subManifest: CdmManifestDeclarationDefinition = cdmManifest.subManifests.allItems[0];
        expect(subManifest.getName())
            .toEqual('sub folder declaration');
        expect(subManifest.explanation)
            .toEqual('test sub explanation');
        expect(subManifest.definition)
            .toEqual('test definition');
    });
});
